# The Delivery Gap Toolkit

Companion tools and guides for *The Delivery Gap: Speed and Certainty in the Age of AI* by Brenn Hill.

AI makes code generation fast. This toolkit makes verification keep up.

---

## Get Started

**The fastest path:** Clone this repo, open it with [Claude Code](https://claude.ai/claude-code), [Cursor](https://cursor.com), or any AI tool that reads `CLAUDE.md`. The AI will walk you through setting up verification infrastructure for your project — policy, gates, measurement — step by step.

```bash
git clone https://github.com/brennhill/Delivery-Gap-Toolkit.git
# Open with your AI coding tool and follow the prompts
```

**Without AI:** Start with the [quick-start guide](quick-start/) for your language, then work through the sections below.

> **Warning:** This toolkit is a starting point, not a finish line. Tier 0 gates catch the cheapest failures. Real verification requires investment in contract gates, invariant tests, and review culture. Do not install this and assume you are safe.

---

## What's Inside

### [AI Policy](ai-policy/)
A defensible AI policy template you can present to leadership — pre-filled with reasoning, not blank fields. Includes a regulatory checklist (HIPAA, SOC2, FedRAMP, GDPR, PCI DSS).

### [Quick Start Guides](quick-start/)
Opinionated Tier 0 setup guides for TypeScript, Python, Go, and JVM. Each tells you exactly what to install and why. One tool per job, no decision fatigue.

### [Quality & Correctness Gates](quality-correctness-gates/)
Gate tooling recommendations by language (Tiers 0-3), an agent production readiness checklist, and an installable multi-pass AI code review tool.

### [Measurement Guidance](measurement-guidance/)
What to measure, which established tools to use (DORA ecosystem), how to see what your CI caught, and how to run a 15-minute weekly review. No custom scripts — we point you to tools that have solved measurement properly.

### [Specs & Process](specs-and-process/)
The four-phase feature definition process: Intent, Behavioral Spec, Design, Implementation. Includes Claude Code slash commands (`/feature`, `/plan`, `/build`) and spec templates.

### [Templates](templates/)
Review checklists, rollout memo for leadership, first-week AI onboarding guide.

### [Worked Examples](tools/)
Invariant, contract, and eval test examples you can adapt for your domain.

---

## The Spec Template

The [Context-Anchor Spec](templates/specs/swe/01-one-page-spec-template.md) has 12 sections split into two blocks:

**Human context (sections 1-4)** comes first: who this is for, what success looks like, who owns it, how to roll back.

**Machine execution (sections 5-12)** comes last: model anchors, entities, scope, constraints, style rules, error contracts, edge cases, acceptance criteria. LLMs exhibit recency bias — placing these last puts them in the strongest position when the AI starts generating code.

Each machine section prevents a specific class of AI hallucination:

| Section | Without it, the AI will... |
|---------|---------------------------|
| Model Anchors | Invent its own architecture instead of following existing patterns |
| Key Entities | Make up names and relationships that don't match the domain |
| Scope Boundaries | Build features you explicitly excluded |
| Constraints | Violate security, SLA, or compliance requirements |
| Style/Architecture Rules | Ignore module boundaries and conventions |
| Error Contract | Invent a different error shape in every function |
| Edge Cases | Ignore boundary conditions and failure paths |
| Acceptance Criteria | Produce code that can't be deterministically verified |

---

## Key Research

### The delivery gap is real

| Study | Finding |
|-------|---------|
| Faros AI (10K developers, 1,255 teams) | PR volume +98%, net throughput: zero |
| Uplevel (800 developers) | 41% increase in bug rate after Copilot adoption |
| GitClear (211M changed lines, 2020-2024) | Code churn doubled; refactoring collapsed |
| NAV IT (20 months, 4,000 developers) | No measurable productivity change |
| CircleCI (9M workflows) | Top 5% at +97% throughput; median at +4% |

### Why gates matter more for AI code

AI-generated code fails systematically, not randomly. The same model produces the same blind spots every time.

| Study | Finding |
|-------|---------|
| [Wu et al., 2024](https://arxiv.org/abs/2407.02209) | LLMs converge on narrower patterns than human developers collectively produce |
| [Dakhel et al., 2025](https://arxiv.org/abs/2508.21634) | 500K+ samples: AI and human defect profiles are complementary |
| [Tamberg et al., 2025](https://arxiv.org/abs/2512.05239) | 10 systematic AI bug patterns including missing corner cases and hallucinated objects |
| [CodeRabbit, 2025](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) | AI code: 2.29x more concurrency issues, 2.25x more business logic errors |
| [Ullah et al., 2025](https://arxiv.org/abs/2510.26103) | 4,241 CWE instances across 77 vulnerability types in AI-generated code |

**Homogeneous generation demands heterogeneous verification.** The gate tiers in this toolkit compensate for the failure-mode diversity that human teams provided accidentally.

---

## External Resources

### From model providers

| Provider | Guide |
|----------|-------|
| OpenAI | [Monitoring coding agents for misalignment](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/) |
| OpenAI | [Practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) |
| Anthropic | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) |
| Anthropic | [Building Effective AI Agents](https://resources.anthropic.com/building-effective-ai-agents) |
| Anthropic | [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) |
| Google | [ADK Safety and Security](https://google.github.io/adk-docs/safety/) |

### Standards

| Standard | URL |
|----------|-----|
| OWASP Top 10 for Agentic Applications | [owasp.org](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) |
| DORA Metrics | [dora.dev](https://dora.dev/guides/dora-metrics/) |
| OpenTelemetry GenAI | [opentelemetry.io](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-metrics/) |

---

## License

Apache 2.0. See [LICENSE](LICENSE).
