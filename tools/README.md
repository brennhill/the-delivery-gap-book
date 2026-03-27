# Tools — Repo-Wide Index

This directory is the entry point for runnable tools, scripts, and reference implementations across the repository.

Use it when you want the fast answer to:

- what can I run right now,
- which part of the control layer it belongs to,
- and where the implementation actually lives.

---

## Quality-correctness gate tools

These live in [`../quality-correctness-gates/`](../quality-correctness-gates/).

- **Agent production checklist** — [`../quality-correctness-gates/agent-production-checklist.md`](../quality-correctness-gates/agent-production-checklist.md)
- **PR size limits** — [`../quality-correctness-gates/pr-size-limits/`](../quality-correctness-gates/pr-size-limits/)
- **Multi-pass review** — [`../quality-correctness-gates/multi-pass-review/`](../quality-correctness-gates/multi-pass-review/)
- **Agent monitoring** — [`../quality-correctness-gates/agent-monitoring/`](../quality-correctness-gates/agent-monitoring/)
- **Observability** — [`../quality-correctness-gates/observability/`](../quality-correctness-gates/observability/)
- **Agent security** — [`../quality-correctness-gates/agent-security/`](../quality-correctness-gates/agent-security/)
- **By language defaults** — [`../quality-correctness-gates/by-language/`](../quality-correctness-gates/by-language/)

These answer: what should block, what should escalate, and what should be observable before a change reaches production.

---

## Templates

The reusable process artifacts live in [`../templates/`](../templates/).

- specs
- review rubrics
- scorecards
- rollout memos
- onboarding guides

These are not scanners or scripts, but they are still part of the machine-checkable system because they define what the checks should enforce.

---

## Worked examples in this directory

### invariant-examples/

Reference implementations for tests that are easier to understand with running code than prose.

- [balance-transfer](invariant-examples/balance-transfer/README.md)
- [event-log](invariant-examples/event-log/README.md)
- [idempotent-webhook](invariant-examples/idempotent-webhook/README.md)
- [rate-limiter](invariant-examples/rate-limiter/README.md)
- [state-machine](invariant-examples/state-machine/README.md)
- [unique-registration](invariant-examples/unique-registration/README.md)

These are examples of the kind of invariant checks the book argues should be automated wherever possible.

---

## Contributing

If you have a worked example of an invariant test, contract gate, policy check, or delivery metric that others could learn from, contributions are welcome. Each addition should be self-contained with its own README explaining what it checks, how to run it, and where it fits in the control layer.
