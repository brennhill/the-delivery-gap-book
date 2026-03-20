# Rust — Gate Tooling

## Tier 0 — Static Analysis

| Tool | Category | URL |
|------|----------|-----|
| rustfmt | Formatter | https://github.com/rust-lang/rustfmt |
| Clippy | Linter (400+ lint rules) | https://github.com/rust-lang/rust-clippy |
| cargo check | Fast type checking without full compile | Built into Cargo |
| cargo-deny | Dependency license + vulnerability audit | https://github.com/EmbarkStudios/cargo-deny |
| cargo-audit | Security vulnerability detection in deps | https://github.com/rustsec/rustsec |
| cargo-udeps | Unused dependency detection | https://github.com/est31/cargo-udeps |
| SonarQube / SonarCloud | Code quality + security | https://www.sonarsource.com |
| Semgrep | Custom rules + OWASP | https://semgrep.dev |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog |

## Tier 1 — Contract Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Pact (pact-rust) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-reference |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff |

## Tier 2 — Invariant Gates

| Tool | What it does | URL |
|------|-------------|-----|
| proptest | Property-based testing | https://github.com/proptest-rs/proptest |
| quickcheck | Property-based testing | https://github.com/BurntSushi/quickcheck |
| cargo-fuzz | Fuzz testing | https://github.com/rust-fuzz/cargo-fuzz |
| Miri | Undefined behavior detection | https://github.com/rust-lang/miri |
| Loom | Concurrency correctness testing | https://github.com/tokio-rs/loom |

## Tier 3 — Policy Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Semgrep | Custom security + policy rules | https://semgrep.dev |
| cargo-deny | License policy enforcement | https://github.com/EmbarkStudios/cargo-deny |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org |
| NVIDIA OpenShell | Agent sandbox (default-deny) | https://github.com/NVIDIA/OpenShell |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
