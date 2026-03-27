# JVM (Java / Kotlin / Scala) — Gate Tooling

> **Last verified:** 2026-03
> For a guided setup, use the AI-assisted setup via CLAUDE.md in the repo root.

## Tier 0 — Static Analysis

| Tool | Category | URL | Verified |
|------|----------|-----|----------|
| SpotBugs | Bug detector (successor to FindBugs) | https://spotbugs.github.io | 2026-03 |
| Error Prone | Compile-time bug detection (Google) | https://errorprone.info | 2026-03 |
| Checkstyle | Style linter (Java) | https://checkstyle.org | 2026-03 |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog | 2026-03 |
| Semgrep | Custom rules + OWASP | https://semgrep.dev | 2026-03 |

## Tier 1 — Contract Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Pact (pact-jvm) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-jvm | 2026-03 |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff | 2026-03 |
| Spring Cloud Contract | Contract testing for Spring | https://spring.io/projects/spring-cloud-contract | 2026-03 |

## Tier 2 — Invariant Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| jqwik | Property-based testing (Java/Kotlin) | https://jqwik.net | 2026-03 |
| JUnit / TestNG | Test framework (invariant tests run here) | https://junit.org | 2026-03 |
| ArchUnit | Architecture rule enforcement | https://www.archunit.org | 2026-03 |

## Tier 3 — Policy Gates

| Tool | What it does | URL | Verified |
|------|-------------|-----|----------|
| Semgrep | Custom security + policy rules | https://semgrep.dev | 2026-03 |
| SpotBugs Security | Security-focused bug detection | https://find-sec-bugs.github.io | 2026-03 |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org | 2026-03 |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
