# JavaScript / TypeScript — Gate Tooling

## Tier 0 — Static Analysis

| Tool | Category | URL |
|------|----------|-----|
| ESLint | Linter (style + correctness) | https://eslint.org |
| Prettier | Formatter | https://prettier.io |
| TypeScript (`tsc --strict`) | Type checker | https://www.typescriptlang.org/tsconfig#strict |
| Biome | Linter + formatter (fast, Rust-based) | https://biomejs.dev |
| ts-prune | Dead code / unused exports | https://github.com/nadeesha/ts-prune |
| knip | Dead code, unused deps, exports | https://knip.dev |
| SonarQube / SonarCloud | Code quality + security | https://www.sonarsource.com |
| Codacy | Automated code review | https://www.codacy.com |
| Snyk | Dependency vulnerabilities | https://snyk.io |
| Semgrep | Custom rules + OWASP | https://semgrep.dev |
| TruffleHog | Secret detection | https://github.com/trufflesecurity/trufflehog |
| detect-secrets | Secret detection | https://github.com/Yelp/detect-secrets |
| npm audit | Dependency audit | Built into npm |

## Tier 1 — Contract Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Pact (pact-js) | Consumer-driven contract testing | https://github.com/pact-foundation/pact-js |
| oasdiff | OpenAPI breaking change detection | https://github.com/Tufin/oasdiff |
| Optic | OpenAPI linting + CI diffs | https://useoptic.com |
| GraphQL Inspector | Schema diff + validation | https://graphql-inspector.com |
| Apollo GraphOS | Schema checks against production traffic | https://www.apollographql.com/docs/graphos |
| GraphQL Hive | Schema registry + breaking change alerts | https://the-guild.dev/graphql/hive |
| Zod / io-ts / Ajv | Runtime schema validation | https://zod.dev |

## Tier 2 — Invariant Gates

| Tool | What it does | URL |
|------|-------------|-----|
| fast-check | Property-based testing | https://fast-check.dev |
| Jest / Vitest | Test framework (invariant tests run here) | https://jestjs.io / https://vitest.dev |
| Playwright | E2E invariant testing | https://playwright.dev |

## Tier 3 — Policy Gates

| Tool | What it does | URL |
|------|-------------|-----|
| Semgrep | Custom security + policy rules | https://semgrep.dev |
| ESLint security plugins | eslint-plugin-security, eslint-plugin-no-secrets | npm |
| OPA / Conftest | Policy-as-code for configs | https://www.openpolicyagent.org |
| Socket | Supply chain attack detection | https://socket.dev |
| NVIDIA OpenShell | Agent sandbox (default-deny) | https://github.com/NVIDIA/OpenShell |

## Tier 4 — Behavioral Gates

Behavioral monitoring, drift detection, and anomaly alerting are infrastructure-level, not language-specific. See [agent-security/](../agent-security/README.md) for the full tooling list covering tracing, LLM-as-judge, canary deployments, and production monitoring.
