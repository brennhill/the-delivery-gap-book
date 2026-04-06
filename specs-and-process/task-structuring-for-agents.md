# Task Structuring for Agents

Agents do not manage complexity — they execute within it. The structure of the task determines the quality of the output. A well-structured task with a mediocre model outperforms a poorly structured task with the best model available.

Airbnb proved this at scale: 3,500 React test files migrated from Enzyme to React Testing Library. The manual estimate was 12-18 months. They completed it in 6 weeks using an AI pipeline with structured per-file steps, rich context injection, and systematic feedback loops. The speed came from the structure, not the model.

---

## Core Principles

### One task, one prompt, one verifiable outcome

Every agent invocation should have a single, testable deliverable. Not "migrate the test suite" — "migrate `UserProfile.test.tsx` from Enzyme to RTL and ensure all existing assertions pass." If you cannot describe what "done" looks like in one sentence, the task is too large.

Spotify's Fleet Management enforces one change per prompt. Combining changes — "migrate the test AND update the component API" — exhausts context or yields partial results. The agent either does the first thing well and the second thing poorly, or does both things halfway.

### Break large work into per-file or per-component units

Airbnb did not give the agent 3,500 files and say "migrate these." They built a pipeline that processed each file as an independent unit. Each unit was:

- **Independently verifiable:** Does this one file's test suite pass?
- **Independently committable:** Can this file be merged without waiting for the rest?
- **Independently recoverable:** If this file breaks, roll it back without affecting the others.

This is the same principle behind small PRs, applied to agent work. The unit of work is the unit of verification.

### Keep each phase under ~400 lines of change

This is the PR size limit applied to agent output. Beyond 400 lines, review quality degrades — reviewers start skimming, and the probability of a missed defect increases nonlinearly. If an agent task will produce more than 400 lines of change, split it into phases.

For migrations, this usually means batching files. For feature work, this means separating infrastructure changes from business logic from tests.

### Front-load context

Give the agent everything it needs upfront rather than expecting it to search. This means:

- The relevant type definitions, not "look in the types directory"
- The specific API contract it must conform to, not "check the API docs"
- Examples of correctly migrated files, not "follow the project conventions"
- The exact linter and test commands to run, not "make sure it passes CI"

Airbnb's pipeline injected rich context for each file: the component source, the existing test, the target testing library's API surface, and examples of previously successful migrations. The agent did not need to explore — it had everything.

---

## Designing the Feedback Loop

Structure without feedback is a one-shot gamble. The feedback loop tells you mid-task whether things are going wrong, before the agent has produced 3,500 files of broken output.

**Signals to monitor during execution:**

| Signal | What it tells you | Action |
|--------|------------------|--------|
| CI failures | The agent's output does not pass existing gates | Stop the batch. Fix the prompt or the pipeline, not each file individually. |
| Lint errors | The agent is violating style or structural conventions | Add the missing convention to the prompt context. |
| Test count changes | Tests were deleted, not migrated | Add a constraint: "The output must have the same number of test cases as the input." |
| Type errors | The agent hallucinated an API or missed a type constraint | Inject the correct type definitions into the prompt context. |
| Review rejection patterns | Reviewers keep flagging the same issue | The prompt is missing a constraint. Add it and re-run the batch. |

**When to stop a batch:**

If three consecutive files fail with the same error class, stop. The problem is systemic — in the prompt, the context, or the model's understanding of the task. Fixing individual files is whack-a-mole. Fix the root cause and restart.

---

## Failure Recovery

Failures in structured agent work are local, not global. That is the entire point of per-file decomposition.

**If one file breaks:** Roll back that file. Do not abandon the migration. Do not re-run the entire batch. Diagnose why that file failed — usually it has a structure the prompt did not anticipate — and either fix the prompt for files like it or handle it manually.

**If a batch breaks:** The prompt or context is wrong for this class of file. Categorize your files (by complexity, by pattern, by component type) and write different prompts for different categories. A single prompt for 3,500 files works only if all 3,500 files have the same structure.

**If the agent produces subtly wrong output that passes tests:** This is the hardest failure mode. Your tests are not testing what you think they are testing. Before running the next batch, add assertions for the specific correctness property the agent violated. Then re-run the failed batch against the stronger test suite.

---

## The Refinement Loop

After a session, ask the agent what was missing from the prompt. Spotify uses this pattern: once the agent completes (or fails) a task, ask it to reflect on what context would have helped it produce better output. The agent's answer is not always right, but it consistently identifies genuine gaps in the prompt context.

**Questions to ask the agent after a session:**

1. "What assumptions did you make that were not stated in the prompt?"
2. "What information did you have to search for that could have been provided upfront?"
3. "Where did you feel uncertain about the correct approach?"

Feed the answers back into the prompt for the next batch. This is iterative prompt refinement driven by the agent's own experience of the task, not by the prompt author's assumptions about what the agent needs.

---

## Putting It Together: Migration Pipeline Example

Airbnb's Enzyme-to-RTL migration pipeline, generalized:

1. **Inventory:** List all files to migrate. Categorize by complexity or pattern if they vary significantly.
2. **Pilot batch:** Run 10-20 files. Review every output manually. Identify failure modes.
3. **Refine prompt:** Fix the gaps the pilot exposed. Add constraints, context, and examples.
4. **Production batch:** Run the next 100 files. Monitor feedback signals (CI, lint, test counts).
5. **Mid-batch check:** After 50 files, review a random sample. If quality has degraded, stop and refine.
6. **Sweep:** Handle the files that failed individually. These are usually edge cases that need manual attention or a specialized prompt.
7. **Verify:** Run the full test suite. Diff test counts against the original. Confirm nothing was silently dropped.

The pipeline is not the agent. The pipeline is the structure that makes the agent's output trustworthy. Without it, you are copy-pasting from ChatGPT into 3,500 files and hoping for the best.
