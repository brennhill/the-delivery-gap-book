# JavaScript / TypeScript — Gate Tooling

> **Last verified:** 2026-03
> For a guided setup, use the AI-assisted setup via CLAUDE.md in the repo root.

## Tier 0 — Static Analysis

| Tool | Category | URL | Verified |
|------|----------|-----|----------|
| Biome | Linter + formatter (fast, Rust-based) | https://biomejs.dev | 2026-03 |
| TypeScript (`tsc --strict`) | Type checker | https://www.typescriptlang.org/tsconfig#strict | 2026-03 |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog | 2026-03 |
| Semgrep | Custom rules + OWASP | https://semgrep.dev | 2026-03 |

## Tier 1 — Contract Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Pact (pact-js) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-js | 2026-03 |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff | 2026-03 |
| Optic | OpenAPI linting + CI diffs | https://useoptic.com | 2026-03 |

## Tier 2 — Invariant Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| fast-check | Property-based testing | https://fast-check.dev | 2026-03 |
| Jest / Vitest | Test framework (invariant tests run here) | https://jestjs.io / https://vitest.dev | 2026-03 |
| Playwright | E2E invariant testing | https://playwright.dev | 2026-03 |

## Tier 3 — Policy Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Semgrep | Custom security + policy rules | https://semgrep.dev | 2026-03 |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org | 2026-03 |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
