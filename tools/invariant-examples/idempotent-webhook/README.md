# Worked Example: Idempotent Webhook Receiver

Runnable companion to **Appendix J** in *AI Augmented Development*.

The book contains the forensic narrative and traces. This repo contains the runnable code so it can stay current, be tested in CI, and be forked without copy-pasting from a PDF.

---

## What this demonstrates

1. The double-charge bug — using `X-Request-Id` as an idempotency key when the provider can change it on retry
2. The correct pattern — verify state against business-entity ID before executing side effects
3. Three stress evals that prove the fix survives partial failures, concurrent retries, and retry pressure

---

## File structure

```
eval_idempotency_stress.py   # The three test cases
webhook_handler.py           # Minimal reference implementation
conftest.py                  # In-memory DB + fake entitlements API fixture
```

---

## Quick start

```bash
pip install pytest
pytest eval_idempotency_stress.py -v
```

---

## `eval_idempotency_stress.py`

```python
"""
Three invariant evals for idempotent webhook processing.

These test correctness under the conditions that actually cause double charges:
  - Provider retry with same idempotency key
  - Two simultaneous retries racing
  - Partial failure: charge succeeded but downstream grant timed out

See Appendix J in AI Augmented Development for the forensic trace and
explanation of why the naive implementation fails.
"""


def test_idempotency_under_retry_pressure(webhook_client, db):
    """Same idempotency key sent twice must produce exactly one charge."""
    payload = {"invoice_id": "inv_789", "amount": 100}
    # Use the business entity ID as the idempotency key, NOT the provider's
    # X-Request-Id header — which changes on retry (that's the original bug).
    idempotency_key = "inv_789"

    result1 = webhook_client.post(payload, idempotency_key=idempotency_key)
    result2 = webhook_client.post(payload, idempotency_key=idempotency_key)

    assert result1.status in (200, 202)
    assert result2.status in (200, 202, 409)  # Accepted or conflict — never 500
    assert db.payments.count(invoice_id="inv_789") == 1
    assert db.entitlements.count(invoice_id="inv_789") == 1  # Grant also idempotent


def test_concurrent_retry_idempotency(webhook_client, db):
    """Two simultaneous retries with the same key must not double-charge."""
    import threading

    payload = {"invoice_id": "inv_790", "amount": 100}
    idempotency_key = "inv_790"
    results = []

    def do_call():
        results.append(webhook_client.post(payload, idempotency_key=idempotency_key))

    t1 = threading.Thread(target=do_call)
    t2 = threading.Thread(target=do_call)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    statuses = {r.status for r in results}
    assert statuses <= {200, 202, 409}, f"Unexpected statuses: {statuses}"
    assert db.payments.count(invoice_id="inv_790") == 1  # Still only one charge
    assert db.entitlements.count(invoice_id="inv_790") == 1


def test_partial_failure_recovery(webhook_client, db):
    """
    Charge succeeded but entitlement grant timed out before the first attempt
    completed. On retry: must NOT re-charge, MUST complete the grant.

    This is the scenario the naive implementation gets wrong:
    - Charge: verified idempotent (correctly skipped)
    - Grant: not checked — runs again and either fails or double-grants

    The correct behavior: verify BOTH side effects before deciding what to do.
    """
    payload = {"invoice_id": "inv_791", "amount": 100}
    idempotency_key = "inv_791"

    # Simulate: charge wrote successfully, entitlement call timed out
    db.payments.insert(invoice_id="inv_791", status="SUCCESS")
    # entitlements table is intentionally empty — grant never completed

    result = webhook_client.post(payload, idempotency_key=idempotency_key)

    assert result.status in (200, 202, 409)
    assert db.payments.count(invoice_id="inv_791") == 1   # No double charge
    assert db.entitlements.count(invoice_id="inv_791") == 1  # Grant completed on retry
```

---

## `webhook_handler.py`

Reference implementation of the "verify state first" pattern.

```python
"""
Idempotent webhook handler reference implementation.

The key design decision: idempotency key is the business entity ID (invoice_id),
not the provider's X-Request-Id header. The provider can change the request ID
on retry. The invoice ID is stable.

On every request:
  1. Check if charge already exists for this invoice_id
  2. Check if entitlement grant already exists for this invoice_id
  3. Execute only the missing steps

This means the handler is safe to call multiple times with the same payload.
"""

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class WebhookResult:
    status: int
    message: str


def handle_invoice_paid(
    invoice_id: str,
    amount_cents: int,
    db,
    entitlements_api,
    verify_timeout_ms: int = 2000,
) -> WebhookResult:
    """
    Process an invoice.paid event idempotently.

    Args:
        invoice_id: Business entity ID — used as idempotency key
        amount_cents: Amount to charge
        db: Database client
        entitlements_api: Entitlements service client
        verify_timeout_ms: Timeout for state-verification queries.
                           Must fit within the webhook's SLA budget.
                           If exceeded, return 503 (retriable) not 500 (fatal).
    """
    # --- Step 1: Verify charge state ---
    try:
        payment = db.payments.get(
            invoice_id=invoice_id,
            timeout_ms=verify_timeout_ms,
        )
    except TimeoutError:
        # State-verification query timed out. Return retriable 503.
        # Do NOT charge — we don't know whether we already charged.
        return WebhookResult(503, "State verification timed out — safe to retry")

    charge_needed = payment is None

    # --- Step 2: Verify entitlement state ---
    try:
        entitlement = db.entitlements.get(
            invoice_id=invoice_id,
            timeout_ms=verify_timeout_ms,
        )
    except TimeoutError:
        return WebhookResult(503, "State verification timed out — safe to retry")

    grant_needed = entitlement is None

    # --- Step 3: Execute only missing steps ---
    if charge_needed:
        db.payments.insert(
            invoice_id=invoice_id,
            amount_cents=amount_cents,
            status="SUCCESS",
        )

    if grant_needed:
        # Pass the same business-entity key to the entitlements API.
        # If it supports idempotency, great. If not, the check above is the guard.
        entitlements_api.grant_access(
            invoice_id=invoice_id,
            idempotency_key=invoice_id,
        )

    if not charge_needed and not grant_needed:
        return WebhookResult(409, "Already processed — idempotent skip")

    return WebhookResult(202, "Accepted")
```

---

## `conftest.py`

```python
"""
pytest fixtures: in-memory database and fake entitlements API.
"""
import pytest
from webhook_handler import handle_invoice_paid


class InMemoryTable:
    def __init__(self):
        self._rows = []

    def insert(self, **kwargs):
        self._rows.append(kwargs)

    def get(self, timeout_ms=None, **filters):
        for row in self._rows:
            if all(row.get(k) == v for k, v in filters.items()):
                return row
        return None

    def count(self, **filters):
        return sum(
            1 for row in self._rows
            if all(row.get(k) == v for k, v in filters.items())
        )


class InMemoryDB:
    def __init__(self):
        self.payments = InMemoryTable()
        self.entitlements = InMemoryTable()


class FakeEntitlementsAPI:
    def __init__(self, db):
        self._db = db

    def grant_access(self, invoice_id, idempotency_key=None):
        if not self._db.entitlements.get(invoice_id=invoice_id):
            self._db.entitlements.insert(invoice_id=invoice_id, status="GRANTED")


class WebhookClient:
    def __init__(self, db):
        self._db = db
        self._entitlements = FakeEntitlementsAPI(db)

    def post(self, payload, idempotency_key):
        return handle_invoice_paid(
            invoice_id=idempotency_key,
            amount_cents=payload["amount"],
            db=self._db,
            entitlements_api=self._entitlements,
        )


@pytest.fixture
def db():
    return InMemoryDB()


@pytest.fixture
def webhook_client(db):
    return WebhookClient(db)
```

---

## What the book says vs. what this code adds

| Book (Appendix J) | This repo |
|---|---|
| Forensic traces showing the bug | Runnable handler that implements the fix |
| "Verify state before retry" pattern | `handle_invoice_paid()` applying that pattern |
| Three stress eval scripts | `conftest.py` fixtures that make them runnable |
| Conceptual explanation of partial failure | `test_partial_failure_recovery` proving it works |

---

## Updating this example

When idempotency patterns evolve (new provider retry behaviors, async webhook queues, event sourcing), update this repo rather than the book. The book's forensic narrative stays stable; the implementation can track current practice.

---

*From [AI Augmented Development](https://aiaugmenteddevelopment.com) by Brenn Hill.*
