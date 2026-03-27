# PHP — Gate Tooling

> **Last verified:** 2026-03
> For a guided setup, use the AI-assisted setup via CLAUDE.md in the repo root.

## Tier 0 — Static Analysis

| Tool | Category | URL | Verified |
|------|----------|-----|----------|
| PHPStan | Static type analyzer | https://phpstan.org | 2026-03 |
| PHP CS Fixer | Formatter | https://cs.symfony.com | 2026-03 |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog | 2026-03 |
| Semgrep | Custom rules + OWASP | https://semgrep.dev | 2026-03 |

## Tier 1 — Contract Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Pact (pact-php) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-php | 2026-03 |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff | 2026-03 |

## Tier 2 — Invariant Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Eris | Property-based testing | https://github.com/giorgiosironi/eris | 2026-03 |
| PHPUnit | Test framework (invariant tests run here) | https://phpunit.de | 2026-03 |

## Tier 3 — Policy Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Semgrep | Custom security + policy rules | https://semgrep.dev | 2026-03 |
| Psalm (taint analysis) | Security taint tracking | https://psalm.dev/docs/security_analysis/ | 2026-03 |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org | 2026-03 |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
