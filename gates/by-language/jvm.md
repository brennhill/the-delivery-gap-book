# JVM (Java / Kotlin / Scala) — Gate Tooling

## Tier 0 — Static Analysis

| Tool | Category | URL |
|------|----------|-----|
| Checkstyle | Style linter (Java) | https://checkstyle.org |
| ktlint | Kotlin linter + formatter | https://pinterest.github.io/ktlint/ |
| Scalafmt | Scala formatter | https://scalameta.org/scalafmt/ |
| SpotBugs | Bug detector (successor to FindBugs) | https://spotbugs.github.io |
| Error Prone | Compile-time bug detection (Google) | https://errorprone.info |
| PMD | Code quality rules | https://pmd.github.io |
| Detekt | Kotlin static analysis | https://detekt.dev |
| SonarQube / SonarCloud | Code quality + security | https://www.sonarsource.com |
| Codacy | Automated code review | https://www.codacy.com |
| Snyk | Dependency vulnerabilities | https://snyk.io |
| Semgrep | Custom rules + OWASP | https://semgrep.dev |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog |
| OWASP Dependency-Check | Dependency vulnerability scan | https://owasp.org/www-project-dependency-check/ |
| Gradle / Maven dependency audit | Built-in dependency analysis | Built into build tools |

## Tier 1 — Contract Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Pact (pact-jvm) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-jvm |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff |
| Spring Cloud Contract | Contract testing for Spring | https://spring.io/projects/spring-cloud-contract |
| gRPC + proto diff | gRPC schema validation | https://grpc.io |

## Tier 2 — Invariant Gates

| Tool | What it does | URL |
|------|-------------|-----|
| jqwik | Property-based testing (Java/Kotlin) | https://jqwik.net |
| ScalaCheck | Property-based testing (Scala) | https://scalacheck.org |
| JUnit / TestNG | Test framework (invariant tests run here) | https://junit.org |
| ArchUnit | Architecture rule enforcement | https://www.archunit.org |
| Temporal (Java SDK) | Durable execution / workflow invariants | https://temporal.io |

## Tier 3 — Policy Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Semgrep | Custom security + policy rules | https://semgrep.dev |
| SpotBugs Security | Security-focused bug detection | https://find-sec-bugs.github.io |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org |
| NVIDIA OpenShell | Agent sandbox (default-deny) | https://github.com/NVIDIA/OpenShell |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
