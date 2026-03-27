# AI-Assisted Development Policy

> **WARNING: This is a starting point, not legal advice. Have your legal and compliance team review before adopting.**
>
> Last updated: [date]

---

## 1. Purpose

This policy establishes guardrails for AI-assisted software development so that teams can move faster without sacrificing delivery stability. It exists because the evidence is clear: organizations that adopt AI tooling without verification infrastructure see negative outcomes (DORA 2025 found -7.2% delivery stability for teams that adopted AI without foundational capabilities), while organizations that pair AI with strong gates and human review capture real productivity gains. This policy ensures we are in the second group.

## 2. Approved Tools

Teams may use the following categories of AI coding tools:

| Category | Examples | Approval Level |
|---|---|---|
| **IDE-integrated assistants** | GitHub Copilot, Cursor, Cody | Approved for all teams |
| **CLI agents** | Claude Code, Aider, Codex CLI | Approved for all teams |
| **Background/autonomous agents** | Devin, Copilot Workspace, Codex | Requires Tier 2+ gate coverage before deployment (see Section 5) |

**Why this default:** Every organization generating substantial value from AI (Spotify, Stripe, Anthropic, OpenAI) uses single-agent architecture with human review at merge time. Background agents that generate PRs without gate coverage produce volume without throughput — Faros found PR volume can increase 98% with net throughput of zero when verification infrastructure is absent.

Teams may request additional tools through [tooling review process/team]. Approved tools must offer enterprise terms or be self-hosted.

## 3. What AI May and May Not Do

AI-assisted development follows the same service tier model used for change management:

| Service Tier | AI Scope | Requirements |
|---|---|---|
| **Tier 1** — Low-risk services, internal tools, prototypes | AI may generate code freely | Standard CI gates must pass |
| **Tier 2** — Customer-facing services, shared libraries | AI may generate code with constraints | Written spec describing intended behavior + human review |
| **Tier 3** — Core platform, payments, auth, data pipelines | AI may generate code with full oversight | Full spec + senior engineer review + all gate tiers passing |

**Why this default:** Risk-proportionate controls prevent both over-restriction (which kills adoption) and under-restriction (which kills stability). The tiering ensures AI is used most freely where the blast radius is smallest.

**AI must not:**
- Commit directly to protected branches without human review
- Disable, skip, or modify CI gates or linting rules
- Access production credentials or environments
- Generate code that handles secrets, auth tokens, or encryption keys without senior review
- Be used as the sole reviewer of its own output

## 4. Human Review Requirement

**All AI-generated code must be reviewed by a human before merge. No exceptions.**

This applies regardless of how the code was generated — autocomplete, chat, CLI agent, or background agent. The reviewer must understand what the code does and why it was written, not merely confirm that CI passed.

**Why this default:** Every company successfully using AI at scale enforces human review at merge time. This is not a trust issue with AI — it is an engineering discipline issue. Code review catches intent misalignment that no automated gate can detect. The moment you remove human review, you convert AI's speed advantage into a defect multiplication advantage.

## 5. Verification Infrastructure Required

Before any team uses AI-assisted development, the following minimum CI gates must be in place and **blocking** (not advisory):

**Required (Tier 0 — non-negotiable):**
- [ ] Linting (language-appropriate, e.g., ESLint, Ruff, Clippy)
- [ ] Type checking (TypeScript strict, mypy, etc.)
- [ ] Secret detection (e.g., Gitleaks, TruffleHog)
- [ ] Dependency vulnerability scanning

**Recommended (Tier 1):**
- [ ] Unit test suite with coverage threshold
- [ ] Build verification (the artifact compiles/bundles)
- [ ] SAST (static application security testing)

**Required for Tier 2+ services:**
- [ ] Integration tests
- [ ] Contract tests (for services with downstream consumers)
- [ ] Performance regression tests (for latency-sensitive paths)

**Why this default:** AI generates code faster than humans can review it. Without automated gates catching the mechanical errors (type mismatches, style violations, leaked secrets), reviewers are overwhelmed by volume and miss the substantive issues. Gates handle the objective checks so humans can focus on intent and design.

## 6. Data and Privacy

Code sent to AI providers is subject to each provider's data handling terms. Teams must be aware of what leaves the network.

**Default policy:**
- Code sent to AI providers via approved tools is acceptable for Tier 1 services, provided the tool's enterprise agreement includes a no-training clause.
- Teams handling PII, PHI, or regulated data must use enterprise-tier tools with data processing agreements, or self-hosted/on-premise models.
- Proprietary algorithms, trade secrets, and security-critical code (auth, encryption) should be flagged for review before sending to external AI providers.
- AI-generated code is subject to the same IP review as human-written code.

**Why this default:** Most enterprise AI tool agreements include no-training clauses, but the terms vary. The risk is not theoretical — it is contractual and regulatory. See the [Regulatory Checklist](regulatory-checklist.md) for framework-specific requirements.

## 7. Measurement

We track system-level indicators of AI-assisted delivery health. We do not surveil individual developers.

**What we track:**
- CI gate catch rate (what percentage of PRs are caught by automated gates before review)
- Review turnaround time (are reviewers keeping up with volume)
- Rework rate (percentage of merged PRs that require follow-up fixes)
- Escaped defect rate (issues found in production that should have been caught earlier)

**What we do NOT track:**
- Individual developer AI usage rates
- Lines of code generated by AI vs. human
- AI tool adoption percentages by team or person

**Why this default:** Tracking individual AI usage creates perverse incentives — developers either game the metric or avoid AI to avoid scrutiny. System-level metrics tell you whether your delivery pipeline is healthy regardless of how the code was written. If rework rate is low and review turnaround is manageable, the tools are working. If not, the problem is infrastructure, not individuals.

## 8. Escalation Path

| Question | Contact |
|---|---|
| "Is this tool approved?" | [Engineering tooling team / manager] |
| "Can I use AI for this service tier?" | [Team lead / architect] |
| "What are the data handling terms?" | [Security / legal team] |
| "I found AI-generated code that bypassed review" | [Engineering management + security] |
| "Policy question not covered here" | [Policy owner — name/role] |

## 9. Review Cadence

This policy is reviewed quarterly. AI tooling and capabilities change rapidly — a policy written today may be inadequate or overly restrictive in 90 days.

**Review process:**
- Policy owner triggers review at the start of each quarter
- Review includes: new tool evaluations, incident post-mortems involving AI-generated code, measurement trends from Section 7, and regulatory changes
- Changes are communicated to all engineering teams with a 2-week notice period before enforcement

---

## Adoption Checklist

Before adopting this policy, confirm:

- [ ] Legal/compliance has reviewed Sections 3, 4, and 6
- [ ] [Regulatory checklist](regulatory-checklist.md) has been completed
- [ ] Tier 0 gates (Section 5) are deployed and blocking in CI
- [ ] Escalation contacts (Section 8) have been filled in
- [ ] All engineering teams have been notified
- [ ] Policy owner and review cadence are confirmed
