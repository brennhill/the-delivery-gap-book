# Your First Week Using AI Tools on This Team

A day-by-day guide for engineers joining a team that uses AI-assisted development with verification infrastructure in place.


## Day 1 — Guardrails Before Generation

Your AI tools are already configured. Before you generate anything, understand what catches mistakes after you do.

**What to do:**

1. Run the project's full lint + type-check + test suite locally. Know what passes before AI touches anything.
2. Read the CI pipeline configuration. Identify which quality gates run on every PR (static analysis, contract tests, invariant checks, policy checks).
3. Note the PR size limit. This team enforces a 400-line maximum per pull request. AI makes it trivially easy to generate more — that is not a reason to do so.

**Why this matters:** AI-generated code that passes your eye test but fails the gates is wasted time. Know what the gates check so you write prompts that respect them.


## Day 2 — The Spec-First Habit

Never start a task by opening your AI tool and prompting. Start by filling out the spec template.

**What to do:**

1. Pick a small task from the backlog.
2. Fill out the [one-page spec template](../specs/01-one-page-spec-template.md) before writing or generating any code. Pay particular attention to Section 3 (scope boundaries) and Section 6 (acceptance criteria).
3. Walk through the workflow: spec → AI generation → review → tests → merge. Your spec is your eval — if you cannot test the output against what you wrote in the spec, rewrite the spec.

**Why this matters:** The spec constrains the AI's scope. Without it, generation drifts, PRs balloon, and review time doubles.


## Day 3 — Reading AI Code Critically

AI code that passes tests can still be wrong. Your job is not to approve — it is to verify.

**Known error patterns in AI-generated code:**

Research quantifies what goes wrong. These are the categories to watch for, ranked by frequency:

| Error Category | How Common | What to Look For |
|---|---|---|
| Logic and correctness | 1.75x human rate | Business logic errors, misconfigurations, unsafe control flow |
| Security vulnerabilities | ~40% of outputs affected | SQL injection, XSS, hardcoded credentials, path traversal |
| Hallucinated APIs/packages | ~20% of package references | Nonexistent functions, fabricated library names, wrong method signatures |
| Edge case omissions | ~3x failure rate on complex inputs | Missing null checks, boundary conditions, error handling |
| Duplication over refactoring | 8x increase since 2020 | Copy-pasted blocks instead of extracting shared logic |

Sources: NYU Tandon (2021), CodeRabbit (2025), GitClear (2025), LiveCodeBench, arXiv 2406.10279.

**What to do:**

1. Review a recent AI-generated PR from the team. Scan specifically for the five categories above — not just "does this look right."
2. **Ask the AI to explain its changes.** Before accepting any AI-generated code, ask the AI to walk through what it did and why. If the explanation does not match the code, or if the AI cannot justify a design decision, treat that as a red flag — do not merge until you understand the logic yourself.
3. Watch for automation bias. Stanford research (Perry et al., 2023) found that developers using AI assistants believed their code was *more* secure when it was actually *less* secure. The confidence the tool gives you is not correlated with correctness.
4. Practice on a deliberately flawed example if your team maintains one. If not, ask your onboarding buddy to point you to a PR where AI output required significant revision.

**Why this matters:** The cost of AI-assisted development is not generation — it is review and rework. The faster you develop a critical read, the lower the team's rework rate.


## Day 4 — Cost Awareness

Every change you ship has a cost. AI shifts where the cost falls, but it does not eliminate it.

**What to do:**

1. Run the [cost calculator](../../metrics/cost-per-accepted-change/cost-calculator.py) on one of your merged PRs. Look at where the time went.
2. Understand what "human engineering time" includes: prompting, yes, but also discussion, whiteboarding, spec writing, and the back-and-forth to get the AI output right. Track this honestly.
3. Check the team's current [rework rate](../../metrics/rework-detection/rework-detector.py). Every change you merge contributes to this number. A change that ships fast but gets reverted within 14 days costs more than one that ships slowly and sticks.

**Why this matters:** Speed without verification creates rework. Rework is the most expensive line item in AI-assisted development because it consumes two review cycles instead of one.


## Day 5 — Working Patterns

Now that you understand the guardrails, the spec habit, critical review, and cost structure — here is how to work day-to-day.

**When to use AI:**
- Boilerplate, scaffolding, and repetitive transforms
- First drafts of tests (then verify coverage yourself)
- Exploring unfamiliar APIs or libraries (treat output as a starting point, not an answer)
- Explaining existing code you are reading for the first time

**When to write it yourself:**
- Security-sensitive logic (auth, encryption, access control)
- Business rules that require domain judgment
- Anything where the spec is ambiguous — clarify the spec first, then decide

**When to escalate:**
- AI output looks correct but you are not confident enough to approve it — ask a teammate
- AI output contradicts the spec — the spec might be wrong, or the AI might be wrong. Either way, do not merge until you know which
- AI-generated tests all pass but you suspect they are testing the wrong thing — this is common and worth a second pair of eyes

**What not to do:**
- Do not commit AI output you have not read line by line
- Do not expand scope because generation is cheap — the spec defines the boundary, not the tool's capability
- Do not skip the spec because "it is a small change" — small changes without specs are how rework starts
- Do not trust AI-generated code more because it is verbose or well-commented — length is not a signal of correctness


## Checklist

By end of week, you should be able to answer yes to all of these:

- [ ] I can run the full gate suite locally and interpret the results
- [ ] I have written at least one spec before generating code
- [ ] I have reviewed AI-generated code and identified at least one issue the gates did not catch
- [ ] I have asked the AI to explain a change and verified the explanation against the code
- [ ] I have run the cost calculator on a real PR
- [ ] I know the team's current rework rate
- [ ] I understand when to use AI tools and when to write code myself
