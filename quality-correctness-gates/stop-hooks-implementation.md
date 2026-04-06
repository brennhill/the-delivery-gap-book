# Stop Hook Enforcement

Deterministic, non-bypassable gates that prevent PR creation if verifiers fail. The agent cannot skip them, override them, or argue with them. If a gate fails, the agent either fixes the problem or stops.

This is the enforcement layer. Policy documents say "all PRs must pass linting." Stop hooks make that sentence true.

---

## The Principle

Every verification step must be enforced at the tooling level, not the prompt level. Telling an agent "always run tests before opening a PR" is a suggestion. Configuring a hook that blocks PR creation until tests pass is a gate.

The distinction matters because agents optimize for task completion. If running tests is optional and the agent is stuck on a test failure, it will skip tests and open the PR anyway. Hooks remove that option.

---

## Claude Code: Stop Hooks

Claude Code's hook system runs scripts at defined lifecycle points. The `stop` hook fires when the agent finishes its work, before it reports completion to the user. If the hook script exits non-zero, its output is fed back to the agent as context and the agent continues working.

### Configuration

Add to `.claude/settings.json` in your project root:

```json
{
  "hooks": {
    "stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/stop-gate.sh"
          }
        ]
      }
    ]
  }
}
```

The `matcher` field filters which agent messages trigger the hook. An empty string matches everything — the gate runs every time the agent tries to stop.

### The Gate Script

```bash
#!/usr/bin/env bash
# .claude/hooks/stop-gate.sh
# Runs all verifiers before the agent can complete its task.
# Exit non-zero to block completion and feed output back to the agent.

set -euo pipefail

FAILURES=()

# --- Tier 0: Formatting and Linting ---
echo "Running formatter check..."
if ! npm run format:check 2>&1; then
    FAILURES+=("Formatter: code is not formatted. Run the formatter.")
fi

echo "Running linter..."
if ! npm run lint 2>&1; then
    FAILURES+=("Linter: lint errors found. Fix them before completing.")
fi

# --- Tier 1: Type Checking ---
echo "Running type checker..."
if ! npx tsc --noEmit 2>&1; then
    FAILURES+=("Type checker: type errors found.")
fi

# --- Tier 2: Tests ---
echo "Running tests..."
if ! npm test 2>&1; then
    FAILURES+=("Tests: one or more tests failed.")
fi

# --- Tier 3: Security ---
echo "Running secret scanner..."
if ! npx gitleaks detect --no-git 2>&1; then
    FAILURES+=("Secret scanner: potential secrets detected in code.")
fi

# --- Tier 4: LLM-as-Judge (optional) ---
if [ -f "scripts/llm-judge.py" ]; then
    echo "Running LLM-as-judge..."
    if ! python scripts/llm-judge.py --diff "$(git diff HEAD)" 2>&1; then
        FAILURES+=("LLM-as-judge: intent alignment check failed.")
    fi
fi

# --- Report ---
if [ ${#FAILURES[@]} -gt 0 ]; then
    echo ""
    echo "=== STOP GATE FAILED ==="
    echo "The following verifiers failed. Fix these issues before completing:"
    echo ""
    for failure in "${FAILURES[@]}"; do
        echo "  - $failure"
    done
    echo ""
    echo "Do not skip these checks. Do not disable tests. Fix the root cause."
    exit 1
fi

echo "All gates passed."
exit 0
```

Make it executable:

```bash
chmod +x .claude/hooks/stop-gate.sh
```

### Adapting for Your Stack

Replace the verifier commands with whatever your project uses:

| Language | Formatter | Linter | Type checker | Tests |
|---|---|---|---|---|
| TypeScript | `prettier --check .` | `eslint .` | `tsc --noEmit` | `vitest run` or `jest` |
| Python | `ruff format --check .` | `ruff check .` | `mypy .` or `pyright` | `pytest` |
| Go | `gofmt -l .` | `golangci-lint run` | (compiled) | `go test ./...` |
| Rust | `cargo fmt --check` | `cargo clippy` | (compiled) | `cargo test` |
| Java/Kotlin | `spotless:check` | (included in compile) | (compiled) | `./gradlew test` |

### What Spotify Does

Spotify configures Claude Code stop hooks to run all verifiers automatically before the agent can open a PR. The agent cannot bypass these checks. If a verifier fails, the agent receives the error output and must fix the issue before trying again. This is the enforcement mechanism behind their LLM-as-judge architecture — the judge itself runs as a stop hook.

---

## GitHub Actions: Branch Protection

Stop hooks enforce gates locally during agent sessions. Branch protection enforces gates on the server, regardless of how the PR was created.

### Required Status Checks

```yaml
# .github/workflows/pr-gates.yml
name: PR Gates
on:
  pull_request:
    branches: [main]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: npm ci

      - name: Format check
        run: npm run format:check

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npx tsc --noEmit

      - name: Tests
        run: npm test

      - name: Secret scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  pr-size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check PR size
        run: |
          LINES_CHANGED=$(git diff --stat origin/main...HEAD | tail -1 | awk '{print $4+$6}')
          echo "Lines changed: $LINES_CHANGED"
          if [ "$LINES_CHANGED" -gt 1000 ]; then
            echo "::error::PR exceeds 1,000 lines changed. Break this into smaller PRs."
            exit 1
          elif [ "$LINES_CHANGED" -gt 500 ]; then
            echo "::warning::PR exceeds 500 lines. Consider breaking it up."
          fi
```

### Enabling Branch Protection

In your GitHub repo settings:

1. Go to **Settings > Branches > Branch protection rules**
2. Add rule for `main`
3. Enable **Require status checks to pass before merging**
4. Select the `verify` and `pr-size` jobs as required checks
5. Enable **Do not allow bypassing the above settings** (this prevents admins from merging anyway)
6. Enable **Require branches to be up to date before merging**

With this configuration, no PR merges to main — whether created by a human or an agent — unless all checks pass. The agent cannot merge its own PR by force-pushing or bypassing CI.

---

## What to Gate

Not everything needs to be a blocking gate. Prioritize by failure severity:

| Gate | Block merge? | Rationale |
|---|---|---|
| Formatter | Yes | Zero ambiguity, zero false positives, instant to fix |
| Linter | Yes | Low false positive rate, catches real bugs |
| Type checker | Yes | Catches structural errors that cause runtime failures |
| Tests | Yes | The minimum bar for correctness |
| Secret scanner | Yes | Leaked secrets are irreversible |
| PR size (> 1,000 lines) | Yes | Large PRs have measurably higher defect rates |
| PR size (> 500 lines) | Warn | Flag for attention, don't block |
| LLM-as-judge | Yes (if configured) | Catches intent mismatches deterministic gates miss |
| Visual regression | Yes (if applicable) | Catches rendering failures invisible to other gates |

### The "green CI" trap

A common failure mode: all gates pass, but the agent tested against stale baselines, skipped integration tests, or wrote tests that assert the wrong thing. Green CI is necessary but not sufficient. Gates catch known failure classes. Human review catches the rest.

---

## Testing That Hooks Work

Before trusting your gates, verify they actually block when they should.

### Test 1: Deliberately fail a verifier

```bash
# Introduce a lint error
echo "const x = 1;" >> src/unused-var.ts

# Run the stop gate
bash .claude/hooks/stop-gate.sh
# Expected: exit code 1, linter failure message

# Clean up
git checkout -- src/unused-var.ts
```

### Test 2: Verify branch protection blocks merge

```bash
# Create a branch with a failing test
git checkout -b test-gate-enforcement
# ... break a test ...
git push -u origin test-gate-enforcement
gh pr create --title "Test: gate enforcement" --body "Deliberately failing PR to verify gates block merge"
# Expected: PR status checks fail, merge button disabled
```

### Test 3: Verify hook runs during agent session

Start a Claude Code session with a trivial task. Before the agent completes, check that the stop gate script ran by looking for its output in the agent's conversation. If the gate runs silently and passes, introduce a deliberate failure to confirm it blocks.

---

## Common Mistakes

**Mistake: Making gates optional with override flags.** If the agent can pass `--skip-tests` or set an environment variable to bypass a gate, it will eventually learn to do so. Gates must be unconditional.

**Mistake: Running gates only in CI, not locally.** The agent creates code locally. If gates only run in CI, the agent opens a PR, CI fails, and the agent may not have context to fix it. Local stop hooks catch failures before the PR exists.

**Mistake: Gates that are too slow.** If your gate suite takes 20 minutes, agents will burn tokens waiting. Keep the local stop gate under 2 minutes. Move slow tests (integration, visual regression) to CI where they run asynchronously.

**Mistake: No feedback to the agent.** When a gate fails, the error output must be clear enough for the agent to fix the problem. "Exit code 1" is not feedback. "Linter: unused variable `x` at src/billing.ts:42" is feedback.
