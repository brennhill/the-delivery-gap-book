# Go — Gate Tooling

> **Last verified:** 2026-03
> For a guided setup, use the AI-assisted setup via CLAUDE.md in the repo root.

## Tier 0 — Static Analysis

| Tool | Category | URL | Verified |
|------|----------|-----|----------|
| golangci-lint | Meta-linter (runs 50+ linters) | https://golangci-lint.run | 2026-03 |
| go vet | Built-in correctness checker | Built into Go toolchain | 2026-03 |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog | 2026-03 |
| Semgrep | Custom rules + OWASP | https://semgrep.dev | 2026-03 |

## Tier 1 — Contract Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Pact (pact-go) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-go | 2026-03 |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff | 2026-03 |
| grpcurl + proto diff | gRPC schema validation | https://github.com/fullstorydev/grpcurl | 2026-03 |

## Tier 2 — Invariant Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| rapid | Property-based testing | https://github.com/flyingmutant/rapid | 2026-03 |
| go-fuzz / native fuzzing | Fuzz testing (built in since Go 1.18) | https://go.dev/doc/fuzz/ | 2026-03 |
| testing package | Test framework (invariant tests run here) | Built into Go | 2026-03 |

## Tier 3 — Policy Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Semgrep | Custom security + policy rules | https://semgrep.dev | 2026-03 |
| gosec | Security policy enforcement | https://github.com/securego/gosec | 2026-03 |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org | 2026-03 |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
