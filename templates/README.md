# Templates — Process Artifacts

The Verification Triangle requires three types of process artifacts: specs that define intent before generation, review rubrics that standardize evaluation, and scorecards that make the weekly feedback loop possible.

These templates are the starting point. Customize them for your team, but don't skip them — a team without a spec template defaults to prompt-first development, a team without a scorecard defaults to no feedback loop, and a team without a review rubric defaults to inconsistent quality.

---

## specs/

Spec templates organized by discipline. Each discipline defines its own sections, scoring model, and completeness criteria. See [specs/README.md](specs/README.md) for design rationale.

- **[swe/01-one-page-spec-template.md](specs/swe/01-one-page-spec-template.md)** — The Context-Anchor Spec for software engineering tasks. Eight sections covering context, model anchors, scope boundaries, constraints, style rules, acceptance criteria, rollback, and ownership.

- **[ml-research/01-ml-research-spec-template.md](specs/ml-research/01-ml-research-spec-template.md)** — ML Research Spec for experiments and model training. Three required sections (research direction, success metric, constraints) plus eight optional sections scored only if included.

Enforcement: PRs without a linked spec for Risk Tier 2+ changes go back before review starts. Add a "Spec Link" field to your PR template, required, not optional.

---

## review/

Templates for standardizing how changes are evaluated.

- **[02-provider-agnostic-code-review-template.md](review/02-provider-agnostic-code-review-template.md)** — Code review checklist that works regardless of which AI tool generated the code. Covers correctness, security, performance, and scope.

- **[03-eval-definition-template.md](review/03-eval-definition-template.md)** — Template for defining acceptance criteria and evaluation rubrics. Use this to make "done" testable before implementation starts.

- **[04-trace-failure-taxonomy.md](review/04-trace-failure-taxonomy.md)** — Failure classification for incident review and postmortems. Maps each failure to the five breakdown modes: output trust, gates, human layer, scope, cost.

---

## Weekly Scorecard

The weekly review is 15 minutes, three people (EM, tech lead, one rotating IC), with a pre-read posted the day before. The scorecard shows four numbers, one outlier, and one control tweak.

| Metric | This week | Last week | 4-week trend | Target |
|--------|-----------|-----------|--------------|--------|
| Cost per accepted change | $ | $ | ↑ ↓ → | $ |
| Rework rate | % | % | ↑ ↓ → | < % |
| Defect escape rate | % | % | ↑ ↓ → | < % |
| Change fail rate | % | % | ↑ ↓ → | < % |

The cadence matters more than the sophistication. A team that reviews four rough numbers weekly outperforms a team that reviews perfect dashboards quarterly.

---

## rollout/

**[06-rollout-memo-template.md](rollout/06-rollout-memo-template.md)** — One-page AI rollout memo for leadership.

Three frames that work: (1) generation vs delivery — we're investing in the bottleneck, (2) one metric that matters — cost per accepted change, (3) what to watch for — PR volume drops while accepted changes stay flat.

---

## onboarding/

**[07-first-week-ai-onboarding.md](onboarding/07-first-week-ai-onboarding.md)** — "Your first week using AI tools on this team" day-by-day guide for new engineers joining a team with verification infrastructure.

Five-day onboarding covering guardrails, spec-first workflow, critical review of AI output (with research-backed error taxonomy), cost awareness, and working patterns.

---

## Further Reading

- [GitHub Spec Kit](https://github.com/github/spec-kit) — GitHub's spec-first workflow templates (MIT)
- [OpenSpec](https://github.com/Fission-AI/OpenSpec) — Machine-readable spec layer for existing codebases (MIT)
- [Martin Fowler / ThoughtWorks: Understanding Spec-Driven Development](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
