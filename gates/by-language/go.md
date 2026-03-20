# Go — Gate Tooling

## Tier 0 — Static Analysis

| Tool | Category | URL |
|------|----------|-----|
| gofmt / goimports | Formatter | Built into Go toolchain |
| go vet | Built-in correctness checker | Built into Go toolchain |
| staticcheck | Comprehensive static analyzer | https://staticcheck.dev |
| golangci-lint | Meta-linter (runs 50+ linters) | https://golangci-lint.run |
| gosec | Security linter | https://github.com/securego/gosec |
| deadcode | Dead code detection | https://pkg.go.dev/golang.org/x/tools/cmd/deadcode |
| SonarQube / SonarCloud | Code quality + security | https://www.sonarsource.com |
| Codacy | Automated code review | https://www.codacy.com |
| Snyk | Dependency vulnerabilities | https://snyk.io |
| Semgrep | Custom rules + OWASP | https://semgrep.dev |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog |
| govulncheck | Dependency vulnerability check | https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck |

## Tier 1 — Contract Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Pact (pact-go) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-go |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff |
| grpcurl + proto diff | gRPC schema validation | https://github.com/fullstorydev/grpcurl |

## Tier 2 — Invariant Gates

| Tool | What it does | URL |
|------|-------------|-----|
| rapid | Property-based testing | https://github.com/flyingmutant/rapid |
| go-fuzz / native fuzzing | Fuzz testing (built in since Go 1.18) | https://go.dev/doc/fuzz/ |
| testing package | Test framework (invariant tests run here) | Built into Go |
| Temporal (Go SDK) | Durable execution / workflow invariants | https://temporal.io |

## Tier 3 — Policy Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Semgrep | Custom security + policy rules | https://semgrep.dev |
| gosec | Security policy enforcement | https://github.com/securego/gosec |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org |
| NVIDIA OpenShell | Agent sandbox (default-deny) | https://github.com/NVIDIA/OpenShell |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
