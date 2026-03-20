# Python — Gate Tooling

## Tier 0 — Static Analysis

| Tool | Category | URL |
|------|----------|-----|
| Ruff | Linter + formatter (fast, Rust-based) | https://github.com/astral-sh/ruff |
| mypy | Static type checker | https://mypy-lang.org |
| pyright | Static type checker (Microsoft) | https://github.com/microsoft/pyright |
| Black | Formatter | https://black.readthedocs.io |
| Bandit | Security linter | https://bandit.readthedocs.io |
| vulture | Dead code detection | https://github.com/jendrikseipp/vulture |
| SonarQube / SonarCloud | Code quality + security | https://www.sonarsource.com |
| Codacy | Automated code review | https://www.codacy.com |
| Snyk | Dependency vulnerabilities | https://snyk.io |
| Semgrep | Custom rules + OWASP | https://semgrep.dev |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog |
| detect-secrets | Secret detection | https://github.com/Yelp/detect-secrets |
| pip-audit | Dependency audit | https://github.com/pypa/pip-audit |
| Safety | Dependency vulnerability check | https://github.com/pyupio/safety |

## Tier 1 — Contract Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Pact (pact-python) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-python |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff |
| Schemathesis | API testing from OpenAPI specs | https://schemathesis.readthedocs.io |
| Pydantic | Runtime data validation | https://docs.pydantic.dev |

## Tier 2 — Invariant Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Hypothesis | Property-based testing | https://hypothesis.works |
| pytest | Test framework (invariant tests run here) | https://pytest.org |
| TLA+ | Formal specification | https://lamport.azurewebsites.net/tla/tla.html |

## Tier 3 — Policy Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Semgrep | Custom security + policy rules | https://semgrep.dev |
| Bandit | OWASP-style security checks | https://bandit.readthedocs.io |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org |
| NVIDIA OpenShell | Agent sandbox (default-deny) | https://github.com/NVIDIA/OpenShell |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
