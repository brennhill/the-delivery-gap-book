# Python — Gate Tooling

> **Last verified:** 2026-03
> For a guided setup, use the AI-assisted setup via CLAUDE.md in the repo root.

## Tier 0 — Static Analysis

| Tool | Category | URL | Verified |
|------|----------|-----|----------|
| Ruff | Linter + formatter (fast, Rust-based) | https://github.com/astral-sh/ruff | 2026-03 |
| mypy | Static type checker | https://mypy-lang.org | 2026-03 |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog | 2026-03 |
| Semgrep | Custom rules + OWASP | https://semgrep.dev | 2026-03 |

## Tier 1 — Contract Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Pact (pact-python) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-python | 2026-03 |
| Schemathesis | API testing from OpenAPI specs | https://schemathesis.readthedocs.io | 2026-03 |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff | 2026-03 |

## Tier 2 — Invariant Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Hypothesis | Property-based testing | https://hypothesis.works | 2026-03 |
| pytest | Test framework (invariant tests run here) | https://pytest.org | 2026-03 |

## Tier 3 — Policy Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Semgrep | Custom security + policy rules | https://semgrep.dev | 2026-03 |
| Bandit | OWASP-style security checks | https://bandit.readthedocs.io | 2026-03 |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org | 2026-03 |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
