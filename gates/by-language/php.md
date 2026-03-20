# PHP — Gate Tooling

## Tier 0 — Static Analysis

| Tool | Category | URL |
|------|----------|-----|
| PHP CS Fixer | Formatter | https://cs.symfony.com |
| PHP_CodeSniffer | Linter (style rules) | https://github.com/squizlabs/PHP_CodeSniffer |
| PHPStan | Static type analyzer | https://phpstan.org |
| Psalm | Static type analyzer (Vimeo) | https://psalm.dev |
| Phan | Static analyzer | https://github.com/phan/phan |
| SonarQube / SonarCloud | Code quality + security | https://www.sonarsource.com |
| Codacy | Automated code review | https://www.codacy.com |
| Snyk | Dependency vulnerabilities | https://snyk.io |
| Semgrep | Custom rules + OWASP | https://semgrep.dev |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog |
| composer audit | Dependency vulnerability check | Built into Composer 2.4+ |
| Enlightn (Laravel) | Security + performance audit | https://www.laravel-enlightn.com |

## Tier 1 — Contract Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Pact (pact-php) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-php |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff |

## Tier 2 — Invariant Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Eris | Property-based testing | https://github.com/giorgiosironi/eris |
| PHPUnit | Test framework (invariant tests run here) | https://phpunit.de |
| Pest | Test framework (modern, expressive) | https://pestphp.com |

## Tier 3 — Policy Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Semgrep | Custom security + policy rules | https://semgrep.dev |
| Psalm (taint analysis) | Security taint tracking | https://psalm.dev/docs/security_analysis/ |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org |
| NVIDIA OpenShell | Agent sandbox (default-deny) | https://github.com/NVIDIA/OpenShell |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
