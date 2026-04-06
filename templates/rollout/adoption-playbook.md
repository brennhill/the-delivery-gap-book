# Adoption Playbook

How to roll out AI-assisted development based on what actual companies did, not what vendor marketing suggests. The common thread: make tools available, let utility drive adoption, formalize only after you have evidence of what works.

---

## Phase 1 -- Organic Adoption (Weeks 1-4)

The goal is not adoption. The goal is learning what works for your team before you commit to anything.

### Make tools available, do not mandate them

Webflow made Cursor and ChatGPT Enterprise available to every engineer on day one. No training program. No mandated usage. No "AI-first initiative" announcement. They gave people tools and watched what happened.

This matters because mandating tools before infrastructure exists creates pressure without guardrails. Engineers comply by using the tool; they do not comply by using it well. You get adoption metrics that look great and quality metrics that degrade silently.

### Pre-install and configure

Dropbox achieved 100% developer AI adoption by pre-configuring tools in the development environment. Engineers did not have to request access, install plugins, or figure out API keys. The tools were there, ready to use, with sane defaults.

The barrier to adoption is almost never "engineers don't want AI tools." It is "engineers don't want to spend 45 minutes configuring something that might not help." Remove the friction and let the tool prove its value on its own.

### Seed with opt-in tooling

Webflow introduced an AI-powered PR linter triggered by a GitHub label. Engineers who wanted AI-assisted review added the label. Engineers who did not want it ignored it. No one was forced.

Opt-in tooling serves two purposes: it lets early adopters experiment without disrupting skeptics, and it generates real usage data about where AI adds value on your specific codebase.

**What to do in Phase 1:**

- Provision AI tool licenses for all engineers (IDE assistants, chat interfaces, CLI tools)
- Pre-configure authentication, API keys, and default settings in the development environment
- Create one or two opt-in AI workflows (PR linting, test generation, documentation) that engineers can try without commitment
- Do NOT track individual usage. Do NOT set adoption targets. Do NOT send "have you tried the AI tools?" emails.

---

## Phase 2 -- Champions (Weeks 4-8)

By week four, some engineers are using the tools daily and others have not touched them. That is expected. The daily users are your champions.

### Identify power users organically

Dropbox created an AI Champions program by identifying engineers who were already effective with the tools — not by asking for volunteers. Champions who self-select are often enthusiasts, not necessarily effective practitioners. Champions who emerge from observed results have credibility.

### Champions share configs, prompts, and patterns

The most valuable thing a champion does is not evangelism. It is making their working setup reproducible. Specific CLAUDE.md files, prompt templates, workflow configurations, and "here is how I use this on our codebase" — concrete artifacts, not motivational talks.

### Dedicated teams build infrastructure, not mandates

Spotify did not tell every team to adopt Fleet Management. A dedicated team built it, proved it worked on real migrations, and let adoption follow utility. Teams adopted because the tool saved them months of manual work, not because a VP sent a Slack message.

**What to do in Phase 2:**

- Identify 3-5 engineers who are demonstrably effective with AI tools (shipping faster, fewer rework cycles, positive review feedback)
- Ask them to document their setups: rule files, prompt templates, workflow configurations
- Create a shared channel or repo where champions post working patterns (not tips — working configurations)
- If a team has a large migration, refactoring, or test backlog, offer AI tooling support as a concrete time-saver
- Still do NOT mandate adoption. Still do NOT set targets.

---

## Phase 3 -- Formalize (Weeks 8-12)

Now you have data. Some workflows are clearly better with AI assistance. Some are not. Formalize what works. Do not formalize what does not.

### Baseline before expanding

This is Decision 1 from the book: measure your current delivery metrics before changing anything. If you did not baseline in Phase 1, baseline now. You need the "before" numbers to prove the "after" numbers mean anything.

Metrics to baseline: rework rate, change failure rate, cycle time (PR open to merge), and defect escape rate. If you cannot measure all four, measure what you can. But measure something before you expand.

### Tier your codebase

Not all code deserves the same level of AI autonomy. Stripe tiers access explicitly:

| Tier | Example | AI Access Level |
|------|---------|----------------|
| Low risk | Internal tooling, documentation, developer utilities | Full agent autonomy. Auto-merge with CI gates. |
| Medium risk | Non-critical services, internal APIs | Agent drafts, human reviews. Standard PR process. |
| High risk | Payment flows, auth, PII handling, compliance surfaces | Read-only AI access. Suggestions only. Human writes all changes. |

Start with low-risk repos. Prove the workflow. Expand to medium-risk with stronger gates. Approach high-risk only with verification infrastructure that you trust from months of evidence.

### Make AI competency a hiring signal

Webflow added AI experience to their hiring filters — not as a requirement, but as a signal. This communicates that AI-assisted development is a core competency for the team, not an optional hobby.

This is a formalization step, not a Phase 1 step. You cannot hire for a competency you have not yet defined internally. Define what "effective AI-assisted development" means for your team (through Phases 1 and 2), then look for it in candidates.

**What to do in Phase 3:**

- Baseline delivery metrics if you have not already (rework rate, CFR, cycle time, escape rate)
- Tier your codebase by risk. Assign AI access levels by tier.
- Standardize the champion-developed configurations as team defaults (CLAUDE.md files, rule files, prompt templates)
- Add AI-assisted development to onboarding materials (see the [first-week onboarding guide](../onboarding/07-first-week-ai-onboarding.md))
- Set quarterly review cadence: are the metrics improving, stable, or degrading?

---

## Anti-Patterns

### Mandating adoption without infrastructure

Amazon mandated 80% Kiro usage across engineering. In March 2026, they experienced outages linked to AI-generated code that bypassed insufficient verification gates. The mandate created pressure to use the tool; it did not create infrastructure to verify the output. Adoption without verification is risk without mitigation.

If your CI pipeline does not catch AI-generated defects, mandating AI usage is mandating an increase in escaped defects. Build the gates first. Adoption follows naturally when the workflow is safe and productive.

### Confusing adoption rate with value

Zapier achieved 89% AI adoption and built 800+ internal agents — but adoption was organic, driven by genuine utility. The number is a trailing indicator of value, not a leading indicator. When adoption rate is the target, it becomes Goodhart's Law in action: engineers use the tool to hit the metric, not to produce better outcomes.

Track delivery metrics alongside adoption. If adoption rises but rework rate also rises, adoption is making things worse.

---

## Metrics That Matter

Adoption rate is a vanity metric. Track these instead:

| Metric | Why | Watch For |
|--------|-----|-----------|
| Rework rate | Measures whether AI-generated code survives review | Rising rework = agents producing low-quality output |
| Change failure rate | Measures whether merged code causes incidents | Rising CFR = verification gates are not catching defects |
| Cycle time | Measures end-to-end delivery speed | Falling cycle time with stable quality = the goal |
| Defect escape rate | Measures whether bugs reach production | Rising escapes = agents bypassing or degrading test coverage |
| Cost per accepted change | Combines speed and quality into one number | If cost rises while volume also rises, you are generating waste |

Review these weekly (see the [weekly review guide](../../measurement-guidance/weekly-review-guide.md)). A team that tracks adoption rate without tracking quality is optimizing for the wrong thing.
