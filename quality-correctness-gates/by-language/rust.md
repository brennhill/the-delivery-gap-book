# Rust — Gate Tooling

> **Last verified:** 2026-03
> For a guided setup, use the AI-assisted setup via CLAUDE.md in the repo root.

## Tier 0 — Static Analysis

| Tool | Category | URL | Verified |
|------|----------|-----|----------|
| Clippy | Linter (400+ lint rules) | https://github.com/rust-lang/rust-clippy | 2026-03 |
| rustfmt | Formatter | https://github.com/rust-lang/rustfmt | 2026-03 |
| cargo-audit | Security vulnerability detection in deps | https://github.com/rustsec/rustsec | 2026-03 |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog | 2026-03 |

## Tier 1 — Contract Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Pact (pact-rust) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-reference | 2026-03 |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff | 2026-03 |

## Tier 2 — Invariant Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| proptest | Property-based testing | https://github.com/proptest-rs/proptest | 2026-03 |
| cargo-fuzz | Fuzz testing | https://github.com/rust-fuzz/cargo-fuzz | 2026-03 |
| Miri | Undefined behavior detection | https://github.com/rust-lang/miri | 2026-03 |

## Tier 3 — Policy Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Semgrep | Custom security + policy rules | https://semgrep.dev | 2026-03 |
| cargo-deny | License policy enforcement | https://github.com/EmbarkStudios/cargo-deny | 2026-03 |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org | 2026-03 |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
