---
description: Execute an implementation plan phase by phase with verification between each
---

# Build

You are implementing an approved plan. Execute one phase at a time, verify each phase, and pause for human confirmation before proceeding to the next.

## Input

The user provides a path to a plan file (e.g., `specs/feature-name-plan.md`). The plan file contains a reference to its spec at the top (e.g., `Spec: specs/feature-name.md`).

Read both:
- The plan file (provided by user)
- The spec file (linked from the plan's header)

Read both fully before starting. Understand the intent, constraints, scope boundaries, and blind spots from the spec. Understand the phasing, file changes, and verification criteria from the plan.

If no plan path is provided, check the `specs/` directory for plan files and ask which one to build.

## Rules

- Follow the plan. Do not improvise, add features, or deviate from scope.
- Respect the spec's scope boundaries — do not touch files listed as non-goals.
- Respect the spec's constraints — check your work against "what must NOT happen."
- If you encounter something that doesn't match the plan, STOP. Present the mismatch clearly:
  ```
  Issue in Phase [N]:
  Expected: [what the plan says]
  Found: [actual situation]
  How should I proceed?
  ```
  Do not guess. Wait for the user.
- Do not skip verification steps.
- Do not proceed to the next phase without human confirmation.

## Process

### For each phase:

1. **Announce the phase.** Say what you're about to do, which files will change, and what the expected outcome is.

2. **Implement using strict TDD.** For each change in the phase:
   - **Red:** Write a failing test first that describes the expected behavior. Run it. Confirm it fails.
   - **Green:** Write the minimum code to make the test pass. Run it. Confirm it passes.
   - **Refactor:** Clean up while keeping tests green.

   Do not write implementation code without a failing test first. For changes that are not unit-testable (config, migrations, static assets), document why TDD does not apply and verify through other means. Follow existing code conventions and the spec's style and architecture rules.

3. **Run automated verification.** Execute every automated verification command listed for this phase. If any fail, fix the issue before proceeding. Do not ask the user to fix automated failures — handle them yourself.

4. **Update the plan.** Check off completed automated verification items in the plan file.

5. **Pause for manual verification.** Say:
   ```
   Phase [N] complete.

   Automated verification passed:
   - [list what passed]

   Please check the manual verification items:
   - [list manual items from the plan]

   Let me know when manual testing is done so I can proceed to Phase [N+1].
   ```
   Wait for the user to confirm before continuing.

6. **Commit.** After the user confirms manual verification, commit the phase with a descriptive message referencing the spec:
   ```
   feat([feature-name]): [phase description]

   Phase [N] of specs/[name]-plan.md
   ```

### After all phases:

Run the spec's acceptance criteria as a final check:
1. Contract checks
2. Invariant checks
3. Policy checks

Report the results. If anything fails, investigate and fix before declaring done.

Then tell the user:
- All phases are complete
- Which acceptance criteria passed
- Any issues encountered during implementation
- The feature is ready for code review

## Resuming

If the user re-runs `/build` on a spec with some phases already checked off:
- Trust that completed phases are done
- Pick up from the first unchecked phase
- Only re-verify previous work if something seems wrong
