# Ruby — Gate Tooling

## Tier 0 — Static Analysis

| Tool | Category | URL |
|------|----------|-----|
| RuboCop | Linter + formatter | https://rubocop.org |
| Sorbet | Gradual type checker (Stripe) | https://sorbet.org |
| Brakeman | Security scanner (Rails) | https://brakemanscanner.org |
| Reek | Code smell detection | https://github.com/troessner/reek |
| debride | Dead code / unreachable method detection | https://github.com/seattlerb/debride |
| SonarQube / SonarCloud | Code quality + security | https://www.sonarsource.com |
| Codacy | Automated code review | https://www.codacy.com |
| Snyk | Dependency vulnerabilities | https://snyk.io |
| Semgrep | Custom rules + OWASP | https://semgrep.dev |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog |
| bundler-audit | Dependency vulnerability check | https://github.com/rubysec/bundler-audit |

## Tier 1 — Contract Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Pact (pact-ruby) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-ruby |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff |
| JSON Schema validation | Runtime contract checks | https://github.com/voxpupuli/json-schema |

## Tier 2 — Invariant Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Rantly | Property-based testing | https://github.com/rantly-rb/rantly |
| RSpec | Test framework (invariant tests run here) | https://rspec.info |
| Minitest | Test framework | https://github.com/minitest/minitest |

## Tier 3 — Policy Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Semgrep | Custom security + policy rules | https://semgrep.dev |
| Brakeman | Rails-specific security policy | https://brakemanscanner.org |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org |
| NVIDIA OpenShell | Agent sandbox (default-deny) | https://github.com/NVIDIA/OpenShell |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
