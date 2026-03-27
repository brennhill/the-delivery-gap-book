---
description: Execute an implementation plan phase by phase with verification between each
---

# Build

You are the **orchestrator** for implementing an approved plan. You do not implement phases yourself. You spawn a fresh sub-agent for each phase, verify its work, and manage the progress file. Each phase gets a clean context with maximum leverage.

This follows the RALPH pattern: fresh context per task, progress preserved through git commits and a progress file, not through conversation history.

## Input

The user provides a path to a plan file (e.g., `specs/feature-name-plan.md`). The plan file contains a reference to its spec at the top (e.g., `Spec: specs/feature-name.md`).

Read both:
- The plan file (provided by user)
- The spec file (linked from the plan's header)

Read both fully before starting. Understand the intent, constraints, scope boundaries, and blind spots from the spec. Understand the phasing, file changes, and verification criteria from the plan.

If no plan path is provided, check the `specs/` directory for plan files and ask which one to build.

## The Progress File

Create `specs/[feature-name]-progress.md` before starting Phase 1:

```markdown
# Progress: [feature name]

> Spec: `specs/[feature-name].md`
> Plan: `specs/[feature-name]-plan.md`

## Completed Phases

(none yet)

## Learnings

(none yet)
```

This file is the memory between phases. Each sub-agent reads it. You update it after each phase. It captures what happened, what was surprising, and what the next phase should know.

## Rules

- **You are the orchestrator, not the implementer.** Spawn sub-agents for each phase. Do not write implementation code yourself.
- Follow the plan. Do not improvise, add features, or deviate from scope.
- Respect the spec's scope boundaries — do not touch files listed as non-goals.
- Do not skip verification steps.
- Do not proceed to the next phase without human confirmation.

## Process

### For each phase:

#### 1. Announce the phase

Tell the user what's about to happen:
```
Starting Phase [N]: [descriptive name]
Files: [list from plan]
Expected outcome: [what changes]
Spawning fresh agent...
```

#### 2. Spawn a sub-agent with clean context

Use the Agent tool to spawn a fresh sub-agent. Give it exactly this context:

```
You are implementing Phase [N] of a feature plan. You have a clean context — do not assume knowledge of prior phases. Read the codebase as it is now.

## Your task
[paste the specific phase from the plan, including files, changes, and verification criteria]

## Spec (intent and constraints)
Read the spec at: specs/[feature-name].md
Pay attention to: scope boundaries, "what must NOT happen", and known AI blind spots.

## Progress from prior phases
Read: specs/[feature-name]-progress.md
This contains learnings from prior phases that may affect your work.

## Rules
- Implement ONLY Phase [N]. Do not touch anything outside this phase's scope.
- Use strict TDD where applicable:
  - Red: Write a failing test first. Run it. Confirm it fails.
  - Green: Write minimum code to pass. Run it. Confirm it passes.
  - Refactor: Clean up while keeping tests green.
- For changes that are not unit-testable (config, migrations, static assets), document why TDD does not apply and verify through other means.
- Follow existing code conventions and the spec's style/architecture rules.
- If you encounter something that doesn't match the plan, STOP and report:
  Issue: [what's wrong]
  Expected: [what the plan says]
  Found: [actual situation]
  Do not guess. Do not proceed.
- Run ALL automated verification commands listed for this phase before finishing.
- When done, report: what you changed, what tests pass, any surprises or learnings for future phases.
```

#### 3. Review the sub-agent's work

When the sub-agent completes, review:
- Did it stay within phase scope? (no extra files changed, no scope creep)
- Did automated verification pass?
- Did it report any mismatches or surprises?

If the sub-agent hit an issue and stopped, present it to the user:
```
Issue in Phase [N]:
Expected: [what the plan says]
Found: [actual situation]
How should I proceed?
```
Do not guess. Wait for the user.

#### 4. Run automated verification yourself

Do not trust the sub-agent's self-report alone. Run every automated verification command listed for this phase independently. If any fail, either fix or re-spawn the sub-agent with the failure context.

#### 5. Update the plan and progress file

Check off completed automated verification items in the plan file.

Update `specs/[feature-name]-progress.md`:
```markdown
## Phase [N]: [name] — COMPLETE

**What changed:** [files modified/created]
**Surprises:** [anything unexpected, or "none"]
**Learnings for future phases:** [anything the next agent should know]
```

#### 6. Commit

Commit the phase immediately after automated verification passes. Use a sequential ID so phases are easy to revert individually:

```
feat([feature-name]): [N]/[total] [phase description]

Phase [N] of specs/[name]-plan.md
```

Example: `feat(toolkit-v2): 3/8 Create measurement-guidance directory`

#### 7. Report and optionally pause

```
Phase [N]/[total] committed.

Automated verification passed:
- [list what passed]

Manual verification items (if any):
- [list manual items from the plan]
```

If the plan specifies manual verification for this phase, pause and wait for confirmation. Otherwise, proceed to the next phase automatically. The user can interrupt at any time.

To revert a single phase: `git revert <commit>` — the sequential commit messages make this easy to find.

### After all phases: Integration sweep

Spawn a **final sweep agent** with clean context:

```
You are verifying that a multi-phase feature implementation connects correctly. All phases have been committed individually. Your job is to verify integration — that the pieces work together, not just individually.

Read:
- Spec: specs/[feature-name].md (especially acceptance criteria and blind spots)
- Plan: specs/[feature-name]-plan.md (all phases, for full picture)
- Progress: specs/[feature-name]-progress.md (learnings and surprises)

Then:
1. Read the current codebase state — all changes are committed.
2. Run the spec's acceptance criteria as integration tests.
3. Check for:
   - Cross-phase integration issues (Phase 2 depends on Phase 1's output — does it actually work?)
   - Gaps between phases (anything that fell between the cracks)
   - Spec blind spots (edge cases, concurrency, security, non-prompted concerns)
4. Report: what passes, what fails, what's suspicious.
```

If the sweep finds issues, fix them (spawn another sub-agent if needed) and re-run.

Then tell the user:
- All phases are complete
- Integration sweep results
- Which acceptance criteria passed
- Any issues encountered during implementation
- The feature is ready for code review

## Resuming

If the user re-runs `/build` on a plan with some phases already completed:
- Read `specs/[feature-name]-progress.md` to understand what's done
- Trust that completed phases are done (they're committed)
- Pick up from the first unchecked phase
- The progress file gives the new context everything it needs — no conversation history required

## Why fresh context per phase

Long-running AI sessions degrade. By phase 5 of a sequential implementation, the context is stuffed with diffs, test output, and verification results from phases 1-4. The AI is working with less effective context for the hardest phases.

Fresh context per phase means:
- Every phase gets the full context budget
- The AI reads the codebase as it actually is (post prior commits), not as it remembers it
- No accumulated noise from prior implementation details
- Progress and learnings are preserved in the progress file, not in conversation memory
- If a phase fails badly, you can re-run it with zero contamination from the failed attempt
