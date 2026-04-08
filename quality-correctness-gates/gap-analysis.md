# Gate Tier Gap Analysis: What Open Tooling Covers and What It Doesn't

The six gate tiers define what verification infrastructure you need. This document maps what is well-served by open-source tooling, what requires assembly from parts, and what does not exist yet — informed by what Stripe, Spotify, and Webflow actually built in production.

Last updated: April 2026.

---

## Tier 0: Static Analysis — Solved

**What's needed:** Linting, type checking, secret detection, coverage enforcement, duplication detection, dependency verification, commit size limits.

**Open tooling coverage: Excellent.**

Every component of Tier 0 has mature, battle-tested open-source tooling. ESLint, Ruff, mypy, gofmt for linting. SonarQube Community Edition for multi-language quality analysis. Semgrep for custom security rules. TruffleHog and detect-secrets for secret detection. Istanbul/nyc, coverage.py, go test -cover for coverage enforcement. Stryker, mutmut, cargo-mutants for mutation testing. jscpd for duplication. sloppy-joe, Socket, GuardDog for dependency verification. pre-commit for orchestration.

**Gap: None.** This tier is solved. If your team does not have Tier 0 running in CI, the problem is adoption, not tooling.

---

## Tier 1: Contract Gates — Good, Setup Is Manual

**What's needed:** API schema drift detection, visual regression, consumer-driven contract testing.

**Open tooling coverage: Good.**

Pact for consumer-driven contracts. oasdiff and Optic for OpenAPI diffing. GraphQL Inspector and GraphQL Hive for GraphQL schemas. Playwright, Chromatic, Percy, BackstopJS for visual regression.

**Gap: Discovery.** The tools verify contracts you already have. Nothing scans your codebase and tells you "these 12 endpoints have no contract spec" or "these 3 services communicate but have no contract test." Setup is per-service, per-endpoint, manual. Stripe's 3M+ test suite includes contract validation because engineers built it over years. A team starting from zero has to identify every integration point themselves.

**What would close the gap:** A tool that scans API routes, inter-service calls, and shared schemas, then generates skeleton contract tests or flags endpoints with no coverage.

---

## Tier 2: Invariant Gates — Tooling Exists, Discovery Doesn't

**What's needed:** Property-based testing, business rule verification (idempotency, ordering constraints, state transition validation).

**Open tooling coverage: The testing frameworks exist. The hard part is knowing what to test.**

Hypothesis (Python) and fast-check (JavaScript/TypeScript) are mature property-based testing frameworks. TLA+ handles formal specification for concurrent systems. Standard integration test frameworks can encode invariants.

**Gap: Invariant discovery.** This is the biggest conceptual gap across all six tiers. Tools test invariants you have already identified. Nothing helps you find the invariants you should be testing. The three forcing questions from the book ("What must never happen twice? What must always be true after this operation completes? What breaks if operations run out of order?") are a human exercise. No tool generates "here are your business invariants" from code analysis.

Stripe's invariant coverage exists because engineers identified and encoded business rules over years of incident response. Spotify's verifiers activate based on component contents — but the invariants those verifiers check were defined by humans who understood the business logic.

**What would close the gap:** Static analysis that identifies likely invariant candidates — functions that modify financial state, endpoints that create or delete resources, operations with retry logic — and suggests property-based tests. This does not exist in open source. LLM-as-judge can partially fill this gap by reviewing code and suggesting "this function handles money — do you have an idempotency invariant?" but that is a prompt, not a product.

---

## Tier 3: Policy Gates — Mixed

**What's needed:** Sandbox enforcement, permission boundary enforcement, compliance checks, agent scope constraints.

**Open tooling coverage: Good for policy-as-code. Mixed for agent-specific enforcement.**

OPA and Conftest handle policy-as-code for infrastructure configs. Semgrep handles custom security rules in application code. Docker, gVisor, and Firecracker provide sandbox isolation at different strength levels. NVIDIA OpenShell provides default-deny agent sandboxing with kernel-level enforcement. NeMo Guardrails provides programmable guardrails for LLM systems. CODEOWNERS enforces reviewer requirements on sensitive paths.

**Gap: Agent permission standards.** Stripe built an internal security control framework that blocks destructive MCP tool use at the infrastructure level. There is no open standard for "agent permission manifest" — a declarative file that says "this agent can read these paths, write these paths, call these tools, and nothing else." Every team rolls their own using a combination of Docker configs, tool allowlists, and context file rules.

OpenShell is the closest to a standard, but it is Linux-only and requires kernel-level features (Landlock, Seccomp) that not every deployment environment supports. For macOS development and CI environments running on standard containers, the gap remains.

**What would close the gap:** A cross-platform agent permission manifest format — something like a `.agent-permissions.yaml` — that sandboxing tools, CI systems, and agent harnesses all understand. Declare once, enforce everywhere.

---

## Tier 4: Behavioral Gates — The Biggest Gap

**What's needed:** Trace grading, behavioral baselining, anomaly detection, LLM-as-judge, drift detection, canary analysis, progressive rollout.

**Open tooling coverage: Weakest tier. Components exist but assembly is entirely DIY.**

Langfuse and Arize Phoenix handle trace collection and basic observability. promptfoo and DeepTeam handle adversarial testing and red-teaming. Argo Rollouts and Flagger handle canary deployments. LaunchDarkly (commercial) and open-source feature flag libraries handle progressive rollout.

**Gap: Behavioral baselining and LLM-as-judge are fully DIY.**

No open tool does "here is your agent's baseline behavior over the last 100 sessions — alert when it deviates." You have to:

1. Collect structured traces (Langfuse or Arize Phoenix)
2. Write scripts to compute baselines (median files read, p95 token usage, tool call distribution)
3. Write alerting logic (if files_read > 3x p95, alert)
4. Build an LLM-as-judge pipeline (prompt template + separate model call + logging + retry cap)
5. Wire it all together with your CI and agent harness

Spotify built this in-house. Their judge vetoes 25% of sessions and runs as a Claude Code stop hook. OpenAI built behavioral monitoring using GPT-5.4 Thinking at maximum reasoning effort across tens of millions of interactions. Neither system is open source. The [agent monitoring guide](agent-monitoring/README.md) and [LLM-as-judge implementation](llm-as-judge-implementation.md) in this toolkit provide the pseudocode and architecture — but it is assembly from parts, not a product you install.

**What would close the gap:** An open-source "agent monitor" that takes structured traces as input and provides: automatic baseline computation, anomaly alerting, LLM-as-judge with configurable prompts, a dashboard showing veto rates and behavioral trends over time. This is the single highest-value open-source project missing from the ecosystem.

---

## Tier 5: Human Review — Process Problem, Not Tooling Problem

**What's needed:** Structured review, AI-aware reviewer assignment, multi-perspective review, substantive comment tracking.

**Open tooling coverage: Good for mechanics, weak for AI-specific review.**

GitHub and GitLab provide review infrastructure. CODEOWNERS routes PRs to the right reviewers. Branch protection enforces review requirements before merge.

**Gap: AI-aware review tooling.** Nothing open-source auto-triages "this PR is AI-generated and touches billing — route to a senior reviewer and require substantive comments." CodeRabbit and Anthropic Code Review provide AI-assisted review commercially. The multi-pass review pattern (Basili's perspective-based reading — user, designer, tester passes) is described in the book and the [multi-pass review guide](multi-pass-review/README.md), but it is a process you implement, not a tool you install.

The rubber-stamping problem — reviewers approving AI-generated PRs without substantive comments — is detectable (track approval-without-comment rate) but not prevented by any tool. It is a management problem addressed by the weekly scorecard and review culture, not by software.

**What would close the gap:** An open-source PR triage tool that reads the diff, classifies risk (based on paths changed, code origin, business logic touched), and adjusts reviewer requirements accordingly. High-risk changes get routed to senior reviewers with a mandatory substantive comment. Low-risk changes get lighter review. This would operationalize the risk tiering from the book as automated reviewer assignment.

---

## Summary

| Tier | Coverage | Primary gap |
|------|----------|-------------|
| **0: Static Analysis** | Solved | None — adopt it |
| **1: Contract Gates** | Good | Contract discovery (which endpoints are ungated?) |
| **2: Invariant Gates** | Frameworks exist | Invariant discovery (what business rules need testing?) |
| **3: Policy Gates** | Mixed | Agent permission manifest standard |
| **4: Behavioral Gates** | Weakest | Behavioral baselining + LLM-as-judge as a product |
| **5: Human Review** | Good mechanics | AI-aware PR triage and rubber-stamp detection |

**The two gaps that matter most:** Tier 2 (invariant discovery) and Tier 4 (behavioral baselining + judge). These are where Stripe and Spotify invested the most engineering time, and where the open tooling ecosystem is furthest behind what production teams actually need.

The companion toolkit's [monitoring guide](agent-monitoring/README.md), [judge implementation](llm-as-judge-implementation.md), and [agent production checklist](agent-production-checklist.md) provide the architecture and pseudocode to build a workable version of Tier 4 from open-source parts. It is not turnkey — but it is the best starting point available today.
