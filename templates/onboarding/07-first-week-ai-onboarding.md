# Your First Week Using AI Tools on This Team

A day-by-day guide for engineers joining a team that uses AI-assisted development with verification infrastructure in place.


## Day 1 — Guardrails and Context Before Generation

Your AI tools are already configured. Before you generate anything, understand what catches mistakes after you do — and how the team gives AI context.

**What to do:**

1. Read the team's CLAUDE.md (or AGENTS.md / .cursorrules). This is how the team gives AI tools project context — architecture, conventions, build commands, and what agents should not do. Understand it before you start prompting.
2. Run the project's full lint + type-check + test suite locally. Know what passes before AI touches anything.
3. Read the CI pipeline configuration. Identify which quality gates run on every PR (static analysis, contract tests, invariant checks, policy checks).
4. Note the PR size limit. This team enforces a 400-line maximum per pull request. AI makes it trivially easy to generate more — that is not a reason to do so.

**Why this matters:** AI-generated code that passes your eye test but fails the gates is wasted time. Know what the gates check so you write prompts that respect them. And the context file is what keeps AI output consistent with team conventions — read it first.


## Day 2 — When and How to Specify

Not every task needs a spec document. A clear prompt IS the spec for small, well-understood changes. For complex or risky work, a spec captures what you learned through iteration so the team can review your thinking.

**What to do:**

1. Pick a small task from the backlog. For a Risk Tier 1 change (small, reversible, well-understood), write a clear prompt and go. The prompt is your spec.
2. Pick a slightly larger task. Explore the problem with your AI tool — iterate, discover constraints, understand the shape of the solution. Then fill out the [one-page spec template](../specs/swe/01-one-page-spec-template.md) to document what you learned. Pay particular attention to Section 3 (scope boundaries) and Section 4 (what must NOT happen).
3. Walk through the workflow: explore and iterate, document constraints in a spec, review the spec with a teammate, then implement. Your spec is the receipt of your thinking, not the recipe for the AI.

**Why this matters:** Specs constrain scope and make your assumptions reviewable. But forcing a spec before you understand the problem leads to speculative documents that the AI follows literally. Iterate first, specify second.


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


## Day 4 — Context Management and Collaborative AI Workflows

AI tools are only as good as the context you give them. Learning to manage context effectively is the difference between fighting the tool and flowing with it.

**What to do:**

1. **Context files matter.** Review your project's CLAUDE.md or equivalent. Notice how it shapes AI behavior. Try making a small change to a convention and observe how the AI's output shifts.
2. **Learn your tool's context window.** Every AI tool has a limited context window. For long sessions, context degrades. Learn when to start a fresh session vs. continuing. Practice referencing specific files and code paths in your prompts — Anthropic's research shows file paths and code examples are the single most effective way to anchor AI output.
3. **Collaborative patterns.** Try these workflows: (a) ask the AI to explain existing code before modifying it, (b) ask the AI to critique its own output before you review it, (c) use the AI to write tests first, then implement against them.
4. **Check the team's rework rate.** See `measurement-guidance/` for how to track this. Every change you merge contributes to this number. A change that ships fast but gets reverted within 14 days costs more than one that ships slowly and sticks.

**Why this matters:** Most AI frustration comes from poor context, not poor models. Engineers who manage context well get dramatically better output with less iteration.


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
- Do not skip thinking about scope because "it is a small change" — for small changes, a clear prompt is the spec; for complex changes, write it down
- Do not trust AI-generated code more because it is verbose or well-commented — length is not a signal of correctness


## Checklist

By end of week, you should be able to answer yes to all of these:

- [ ] I can run the full gate suite locally and interpret the results
- [ ] I have read the team's CLAUDE.md or equivalent context file
- [ ] I have completed a small task with just a clear prompt, and a larger task where I iterated then wrote a spec
- [ ] I have reviewed AI-generated code and identified at least one issue the gates did not catch
- [ ] I have asked the AI to explain a change and verified the explanation against the code
- [ ] I have practiced referencing specific file paths and code examples in my prompts
- [ ] I know the team's current rework rate
- [ ] I understand when to use AI tools and when to write code myself
