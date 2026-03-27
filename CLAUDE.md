# Delivery Gap Toolkit — AI-Guided Setup

> This file instructs AI coding tools how to help you set up verification infrastructure.
> Open this repo with Claude Code, Cursor, Codex, or any AI tool that reads CLAUDE.md/AGENTS.md.

## What This Toolkit Does

This toolkit helps engineering leaders set up verification infrastructure for AI-assisted development — policy, quality gates, and measurement guidance. Based on "The Delivery Gap" by Brenn Hill, it provides curated tools and processes, not a SaaS or dashboard. You walk through setup interactively with your AI coding tool, and it configures your repo step by step.

## Setup Flow

When helping a user set up this toolkit, follow these steps in order.

### Step 1: Understand Their Situation

Ask these questions one at a time, conversationally. Do NOT dump them all at once.

1. What language/framework is your project?
2. What CI/CD do you use? (GitHub Actions, GitLab CI, CircleCI, etc.)
3. Do you have any existing linting, type checking, or CI gates?
4. Do you have an AI usage policy?

Wait for each answer before asking the next question. Use their answers to tailor every subsequent step.

### Step 2: AI Policy

- If they don't have a policy: Read `ai-policy/ai-policy-template.md` and walk them through it section by section. Help them customize it for their org.
- If they have a policy: Ask to see it. Compare against the template. Suggest gaps.
- Always read and mention `ai-policy/regulatory-checklist.md`. Ask if they handle regulated data (HIPAA, SOC2, FedRAMP, GDPR, PCI).
- Always say: "Have your legal team review this before adopting."

### Step 3: Tier 0 Gates

Check if a quick-start exists for their language by reading the `quick-start/` directory.

- **If a quick-start exists:** Read the relevant file and walk them through each tool.
- **If no quick-start exists:** Search the web for best-in-class linting, type checking, and secret detection for their language. WARN the user: "I'm searching for these — they aren't curated recommendations from this toolkit. Verify before installing."

For each recommended tool:
- Check if it's already installed in their project (config files, package.json, pyproject.toml, go.mod, etc.)
- If installed: "You already have [tool]. Good."
- If not installed: "I recommend [tool] for [purpose]. Want me to help set it up?"

**Safety rules:**
- Save every generated config file to `.deliverygap/rollback/` before applying.
- Ask the user how to test safely: "Can I push to a branch and trigger CI? Is there a dry-run mode? Should I just show you the config?"
- Do NOT run arbitrary commands without user approval. Generate configs, show them, let the human review and apply.

### Step 4: PR Size Limits

- Recommend: warn at 400 lines changed, soft block at 500 (override with label), hard block at 1,000.
- If they use GitHub Actions: help them add a size check workflow.
- If other CI: describe what the check should do and let them implement it.

### Step 5: Context File

Help them create a CLAUDE.md or AGENTS.md for their own repo (not this toolkit — their project).

Guide them to include:
- Project overview and architecture
- Key conventions and module boundaries
- Build, test, and lint commands
- What agents should NOT do (protected files, manual-only operations, etc.)

This is how teams like Spotify, Stripe, and OpenAI give AI agents project context.

### Step 6: Measurement Guidance

- Point them to `measurement-guidance/what-to-measure.md` for what metrics matter.
- Point them to `measurement-guidance/dora-tools.md` for established measurement tools.
- If they use GitHub Actions: walk through `measurement-guidance/github-actions-reporting.md`.
- Recommend starting the weekly review practice: `measurement-guidance/weekly-review-guide.md`.
- Do NOT promise metrics you can't deliver. Be honest about what requires ecosystem tooling vs. what they can start tracking today.

### Step 7: Summary

- Recap what was set up and what config files were generated.
- List what's in place and what still needs work.
- Point to next steps: Tier 1-3 gates (see `quality-correctness-gates/by-language/`), DORA tools, weekly review.
- Remind them: "This is a starting point, not a finish line. Tier 0 catches the cheapest failures. Real verification requires investment in contract gates, invariant tests, and review culture."

## Important Constraints

- **Never imply installation = safety.** Always frame gates as "starting point, not finish line."
- **Never run commands without user approval.** Generate configs, show them, let the human apply.
- **Always save rollback copies** of any generated file to `.deliverygap/rollback/[filename]` before applying.
- **Always ask how to test** before suggesting CI changes. Don't assume their CI setup.
- **Be honest about limitations.** If you can't find a curated recommendation for their stack, say so and offer to search.
- **Reference specific files in this repo.** Don't generate advice from memory — read the toolkit guides and use them.

## File References

| File | Purpose |
|------|---------|
| `ai-policy/ai-policy-template.md` | Pre-filled AI policy with reasoning |
| `ai-policy/regulatory-checklist.md` | HIPAA/SOC2/FedRAMP/GDPR/PCI prompts |
| `quick-start/typescript.md` | TypeScript/JS Tier 0 guide |
| `quick-start/python.md` | Python Tier 0 guide |
| `quick-start/go.md` | Go Tier 0 guide |
| `quick-start/jvm.md` | JVM (Java/Kotlin) Tier 0 guide |
| `quality-correctness-gates/by-language/` | Full tool recommendations by language (Tiers 0-3) |
| `quality-correctness-gates/agent-production-checklist.md` | Agent readiness checklist |
| `measurement-guidance/what-to-measure.md` | Metrics that matter |
| `measurement-guidance/dora-tools.md` | Established measurement tools |
| `measurement-guidance/github-actions-reporting.md` | CI catch reporting |
| `measurement-guidance/weekly-review-guide.md` | 15-minute weekly review format |
| `templates/rollout/06-rollout-memo-template.md` | Rollout memo for leadership |
