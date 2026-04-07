# Multi-Team Rollout Guide

The [adoption playbook](adoption-playbook.md) covers how a single team moves from organic adoption through formalization. This guide covers how a Director of Engineering or CTO sequences that process across 5, 15, or 50 teams.

The core principle: **start where hallucinations are cheap, build verification there, then scale outward.** You do not roll out AI tooling and verification infrastructure at the same time to every team. You pick teams where AI failures have low blast radius, prove the verification workflow works, and expand with evidence.

---

## Team Selection: Blast Radius First

The first question is not "which team is most excited?" It is "where does an AI hallucination cost the least?"

AI-generated code hallucinates confidently. It invents API calls, misuses libraries, and produces plausible-looking code that is subtly wrong. Your first rollout teams should be in areas where those failures are caught cheaply — not because the teams are less important, but because your verification infrastructure is weakest at the start.

### Selection Criteria

| Criterion | Good first team | Bad first team |
|-----------|----------------|----------------|
| **Blast radius of defects** | Internal dashboard, admin UI, developer tooling, docs | Payment processing, auth, compliance, customer-facing API |
| **Hallucination risk** | UI components, CRUD, data display — wrong output is visible and non-destructive | Financial calculations, security logic, data mutations — wrong output causes real damage |
| **Existing test coverage** | Team already has CI, linting, and reasonable test coverage to build on | Team has no CI pipeline and ships by manual QA |
| **Team disposition** | Pragmatic — willing to try things, willing to report what breaks | Either zealously pro-AI (will skip verification) or actively hostile (will sabotage the pilot) |
| **Codebase risk tier** | Tier 1 (internal tools) or Tier 2 (non-critical services) | Tier 3 (billing, auth, PII, compliance) |

**The ideal first team** builds internal tooling or internal dashboards. If the AI hallucinates a wrong chart label or a broken filter, someone on the team sees it in the next standup. Nobody gets paged. No customer data is corrupted. No compliance violation occurs. The feedback loop is fast and the blast radius is bounded.

**The ideal second team** builds a customer-facing service with moderate risk — a feature that users interact with but where defects cause inconvenience, not damage. This team proves that the verification workflow scales to higher-stakes code.

**The team you approach last** owns billing, authentication, PII handling, or regulatory compliance surfaces. By the time you reach them, your gate tiers are battle-tested, your measurement is running, your champions have documented patterns for your codebase, and you have months of evidence that the process works.

---

## Rollout Waves

### Wave 1: Prove It Works (1-2 teams, weeks 1-12)

**Goal:** Demonstrate that AI-assisted development with verification infrastructure produces measurable results on your codebase, with your engineers, in your CI system. Everything after this wave depends on credible evidence from this one.

**Select:** 1-2 teams building internal tools, admin UIs, developer utilities, or non-critical internal services. Low blast radius. Existing CI. Pragmatic team leads.

**What they do:**
- Follow the [adoption playbook](adoption-playbook.md) phases 1-3 (organic → champions → formalize)
- Stand up Tier 0 gates (linting, type checking, secret detection, coverage floor, commit size limits)
- Stand up Tier 1 gates (contract checks or visual regression, depending on their domain)
- Baseline and track the four delivery metrics weekly
- Document everything: what worked, what broke, what took longer than expected

**What you build during this wave (shared infrastructure):**
- Standardized CI gate configurations that other teams can copy
- CLAUDE.md / context file templates tailored to your org
- A shared channel where Wave 1 engineers post working patterns
- The first version of your weekly scorecard

**Exit criteria:**
- 12 weeks of weekly metric data showing stable or improving delivery quality
- At least 2 gate tiers running in CI and blocking on failure
- At least 1 documented "the gate caught something real" story
- Written assessment of what the next wave needs that this wave did not have

### Wave 2: Scale the Infrastructure (3-5 teams, weeks 8-20)

**Goal:** Prove the workflow works across different team sizes, tech stacks, and risk profiles. Uncover the failure modes that only appear at scale.

**Select:** 3-5 teams across a range of risk levels. At least one customer-facing team. At least one team on a different tech stack than Wave 1.

**Start Wave 2 while Wave 1 is still in progress** — overlap by 4 weeks. Wave 1 teams become your champions and infrastructure advisors. They have the context to onboard Wave 2 teams faster than starting from scratch.

**What Wave 2 teams do:**
- Copy Wave 1's gate configurations and adapt for their stack
- Add Tier 2 gates (invariant tests) for teams with business logic worth protecting
- Customer-facing teams add visual regression if they ship UI
- Weekly metrics from day one (the infrastructure exists now)

**What you build during this wave:**
- Cross-team metric comparison dashboard (or spreadsheet — the tool matters less than the visibility)
- Training materials for Tier 1 and Tier 2 gates based on Wave 1 lessons
- Escalation path for when a gate blocks a deploy and nobody knows why

**New failure modes you will discover in Wave 2:**
- Teams with different CI systems need different gate configurations
- Cross-service contract gates are harder than single-service gates
- The team with no existing tests cannot hit the 90% coverage floor in 4 weeks
- Champion burnout: Wave 1 engineers get asked to help everyone and their own work suffers

**Exit criteria:**
- All Wave 2 teams running Tier 0 + Tier 1 gates in CI
- At least one customer-facing team running Tier 2 gates
- Metric trends across 5+ teams showing consistent direction
- Training materials that a team can self-serve without a champion sitting next to them

### Wave 3: Organizational Default (Remaining teams, weeks 16-30)

**Goal:** AI-assisted development with verification gates becomes the standard workflow, not a pilot.

**Select:** Everyone else, in batches of 3-5 teams at a time.

**What changes in Wave 3:**
- Self-service onboarding: teams read the docs, copy the configs, and start. Champions advise but do not hand-hold.
- Standardized gate templates per tech stack (the output of Waves 1-2)
- New hires onboard into the AI-assisted workflow from day one (see [first-week onboarding guide](../onboarding/07-first-week-ai-onboarding.md))
- Tier 3 (policy) and Tier 4 (behavioral) gates for teams that are ready
- High-risk teams (billing, auth, compliance) join with the strongest gate configurations and the most conservative AI access levels

**Exit criteria:**
- All teams running at least Tier 0 + Tier 1 gates
- Weekly metrics reported org-wide
- Gate health visible on a shared dashboard
- The question shifts from "are we using AI?" to "are our gates catching the right things?"

---

## Timeline Reality

The 30/60/90 plan in the book is for one team. For an organization of 15 teams:

| Milestone | Realistic timeline |
|-----------|-------------------|
| Wave 1 complete (1-2 teams, full verification) | 12 weeks |
| Wave 2 complete (5-7 teams total) | 20 weeks |
| Wave 3 complete (all teams at Tier 0+1 minimum) | 30 weeks |
| Organizational maturity (most teams at Tier 2+, high-risk at Tier 3+) | 9-12 months |

These are not aspirational targets. They assume a dedicated infrastructure investment (at least one engineer spending 50%+ time on shared gate tooling) and leadership support. Without that, add 50%.

**The first team takes 12 weeks. The fifteenth team takes 2 weeks.** The infrastructure, training materials, and organizational muscle built in Waves 1-2 compress onboarding for every subsequent team. This is the compounding return on the early investment.

---

## Handling Resistance

### The team lead who says "we are already fine"

They may be right — for now. Do not force it. Instead, make the org-wide metrics visible. When their peer teams show improving delivery quality, the holdout team either joins voluntarily or becomes visibly behind. Social proof works better than mandates. If they still resist after Wave 2 evidence is visible, have a direct conversation about what specifically concerns them. It is usually one of: "this will slow us down" (show cycle time data from pilot teams), "our code is too complex" (agree — their code may need higher-tier gates, not lower adoption), or "I do not trust the tools" (pair them with a champion for one sprint).

### The senior who has been rubber-stamping AI code

This is a quality problem, not an adoption problem. The weekly scorecard with "PR approval rate with zero substantive comments" (from the gate audit table in Chapter 7) makes rubber-stamping visible. Do not call them out. Let the metric speak. When the team reviews the scorecard and sees a rising approval-without-comment rate, the conversation happens naturally.

### The team that sees gates as bureaucracy

They are usually right that *bad* gates are bureaucracy. The fix is not fewer gates — it is faster gates. If your Tier 0 suite takes 15 minutes, it feels like a tax. If it takes 90 seconds, it feels like a safety net. Invest in gate speed before gate breadth. A team that has fast, useful gates will accept more gates. A team that has slow, noisy gates will resist all gates.

### The enthusiast who skips verification

More dangerous than the skeptic. They generate volume, hit coverage metrics, and produce code that passes CI but tests nothing meaningful. The LLM-as-judge and mutation testing layers are designed for exactly this failure mode. Do not rely on social pressure — build the infrastructure that catches hollow coverage.

---

## What to Build Once vs. Per Team

| Build once (shared infrastructure) | Build per team |
|-------------------------------------|---------------|
| CI gate template configs by language/framework | Team-specific CLAUDE.md / context files |
| Coverage and mutation testing pipeline setup | Team-specific invariant tests (their business rules) |
| Secret detection and dependency verification | Team-specific contract specs (their APIs) |
| Weekly scorecard template and metric collection | Team-specific risk tiering (their codebase) |
| Training materials for each gate tier | Team-specific alert thresholds (their baselines) |
| LLM-as-judge prompt and stop hook scripts | Team-specific review rotation and capacity planning |

The "build once" column is why Wave 1 takes 12 weeks and Wave 3 takes 2 weeks per team. The investment is front-loaded.

---

## Reporting to Leadership

After Wave 1, you have data. Present it as:

1. **Before/after metrics** for the pilot teams (not adoption rate — delivery metrics)
2. **Gate catch stories** — specific examples of defects the gates caught before production
3. **Cost per accepted change trend** — is it going down?
4. **Rollout timeline** — where you are in the wave plan, what is next
5. **Investment ask** — what shared infrastructure you need to build for the next wave

Do not present adoption rate as a success metric. Present delivery quality. If a VP asks "what percentage of engineers are using AI?", redirect: "89% of Wave 1 and 2 teams are using AI with verification gates. Their change failure rate dropped X%. That is the number that matters."

---

## Sources

The rollout patterns in this guide are drawn from published engineering practices at:

- **Spotify:** Organic adoption, dedicated infrastructure team, LLM-as-judge, verification-first rollout
- **Stripe:** Pre-configured tools, devbox isolation, 1,300+ PRs/week with mandatory human review
- **Webflow:** Opt-in tooling, AI PR linter, 89% daily usage through utility not mandate
- **Dropbox:** Pre-installed tools, AI Champions program, 100% adoption through friction removal
- **Zapier:** Company-wide experimentation culture, 800+ internal agents, organic adoption

See the [book's production verification appendix](../../main-book/appendix-verification-in-production.md) for detailed evidence from each company.
