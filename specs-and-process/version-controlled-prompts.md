# Version-Controlled Prompts

Prompts are the intent definition for agent work. An unversioned prompt is untraceable — when the agent produces bad output, you cannot determine whether the problem was the prompt, the model, or the code. Version your prompts like source code, review them like source code, and treat changes to them as changes to your system's behavior.

Spotify learned this during large-scale migrations: the prompts that drove Fleet Management were stored in Git and code-reviewed by the same engineers who reviewed the migration output. The prompt *is* the specification. It deserves the same rigor.

---

## Why This Matters

A single prompt change can affect hundreds or thousands of lines of generated code. This is Horthy's cascade: a bad prompt does not produce one bad line — it produces hundreds of bad lines, all consistently wrong in the same way. The blast radius of an unreviewed prompt change is orders of magnitude larger than an unreviewed code change.

If your prompts live in Slack threads, Notion pages, or someone's clipboard, you have no audit trail. When the output regresses, you cannot diff what changed. When a new team member joins, they cannot see why a prompt was written the way it was. When a model upgrade changes behavior, you cannot reproduce the previous result.

---

## Per-Directory CLAUDE.md Files

Create a CLAUDE.md (or AGENTS.md, or rules file) for a directory when that directory has conventions the agent cannot infer from the code alone. If the conventions are obvious from reading the existing code, you do not need a file — you need the agent to read the code.

**When to create one:**

- The directory has naming conventions, architectural boundaries, or import rules that are not enforced by linting
- There are things the agent must NOT do (protected files, manual-only operations, deprecated patterns it should not propagate)
- The build/test/lint commands for this module differ from the project root
- There are domain-specific constraints (e.g., "this service must not import from the billing module directly")

**When you do NOT need one:**

- The conventions are already enforced by linters, type checkers, or CI gates
- The patterns are obvious from reading three or four files in the directory
- You would be restating what the code already says

**What goes in a CLAUDE.md:**

| Section | What to Include |
|---------|----------------|
| Project overview | One paragraph. What this module does and why it exists. |
| Architecture | Layer structure, module boundaries, data flow direction. |
| Key conventions | Naming, error handling patterns, logging expectations. |
| Build/test/lint | Exact commands. Not "run the tests" — the actual command. |
| What agents must NOT do | Protected files, manual-only operations, patterns to avoid. |
| Module boundaries | What this module may import and what it may not. |

Keep it under 200 lines. If it is longer, you are trying to replace documentation with a context file. The CLAUDE.md is a constraint document, not a wiki.

---

## Rule Files and Cross-Tool Sync

Stripe maintains rule files that sync across Minions, Cursor, and Claude Code. The rules are scoped to subdirectories and file patterns — a rule for `payments/` does not apply to `internal-tools/`. This scoping is critical.

**Scoping rules:**

- Scope rules to the narrowest directory or file pattern that applies. A rule that says "always use structured logging" in the project root wastes context window for every agent invocation, even when the agent is editing a README.
- Use file-pattern matching (e.g., `*.test.ts`, `migrations/*.sql`) when a convention applies to a file type, not a directory.
- Avoid unconditional global rules. Every rule the agent loads costs context window. If a rule applies to 5% of your codebase, scope it to that 5%.

**What makes a good rule:**

- Specific enough that the agent can follow it without judgment calls
- Narrow enough in scope that it does not waste context on unrelated tasks
- Testable — you can verify whether the agent followed the rule by inspecting the output

**What makes a bad rule:**

- "Write clean code" (not actionable)
- "Follow best practices" (the agent will hallucinate what those are)
- "Be careful with security" (no specific constraint to follow)

---

## Prompt Review Process

Diffs on prompt changes should be reviewed with the same rigor as code changes. The review question is not "does this prompt read well?" — it is "will this prompt produce correct output across the range of inputs it will encounter?"

**Review checklist for prompt changes:**

1. **Scope:** Does the prompt constrain what the agent should NOT do? Omitting constraints is the most common prompt failure mode.
2. **Verifiability:** Can you test whether the agent followed this prompt? If not, the prompt is unenforceable.
3. **Edge cases:** What happens when the agent encounters an input the prompt author did not anticipate? Does the prompt fail gracefully or produce silent errors?
4. **Context cost:** How many tokens does this prompt consume? Is every line earning its place in the context window?
5. **Blast radius:** How many files or components will be affected by output generated from this prompt? Higher blast radius demands more review.

**Who reviews prompt changes:**

The engineer who will review the agent's output. They need to understand the intent to evaluate the result. If the prompt author and the output reviewer are different people who never talk, the review is theater.

---

## End-State vs. Step-by-Step

Spotify found that Claude Code performs better with end-state descriptions than with step-by-step instructions. Tell the agent what the result should look like, not the sequence of keystrokes to get there.

**End-state (preferred):**
> "Migrate this component from Enzyme to React Testing Library. The test should render the component, simulate a click on the submit button, and assert that the onSubmit callback was called with the form data. Use screen queries, not wrapper methods."

**Step-by-step (fragile):**
> "Step 1: Remove the Enzyme import. Step 2: Add the RTL import. Step 3: Replace shallow() with render(). Step 4: Replace wrapper.find() with screen.getByRole(). Step 5: ..."

The step-by-step version breaks when the agent encounters a component that does not match the expected structure. The end-state version lets the agent adapt its approach to the actual code.

As models improve, less detail is needed. A prompt that required ten specific instructions in 2024 may need three in 2025. Revisit your prompts when you upgrade models — over-specification becomes a liability when the model is capable of inferring the right approach.

---

## Anti-Patterns

**Overly generic prompts:** "Improve this code" or "Add tests." The agent guesses your intent, and its guess will be wrong in ways you do not notice until production. Every prompt should specify what "done" looks like.

**Overly specific prompts:** Step-by-step instructions that assume a particular code structure. When the agent encounters a file that does not match the assumed structure, it either fails or forces the code into the wrong shape. Specify the outcome, not the steps.

**Prompts without constraints:** "Refactor the authentication module." What must NOT change? What interfaces are public contracts? What performance characteristics must be preserved? A prompt without constraints is a prompt that authorizes the agent to break anything.

**Prompts that assume model behavior:** "You are an expert in X" or "Think step by step." These are cargo cult patterns. They may have helped GPT-3.5 in 2023. Benchmark them against your current model before cluttering every prompt with them.

**One prompt for multiple changes:** Spotify enforces one change per prompt. Combining changes exhausts context or yields partial results. If you find yourself writing "also" in a prompt, split it.
