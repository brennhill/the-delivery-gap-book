# Rework Detection

Classifies merged changes as accepted, rework, or pending based on a 14-day observation window.

## Usage

```bash
# Local repo
python rework-detector.py

# GitHub repo
python rework-detector.py --repo owner/repo

# Custom window and lookback
python rework-detector.py --window 7 --lookback 60

# Output for chaining with cost calculator
python rework-detector.py --json rework.json
```

## Detection Signals

1. **Explicit reverts** — `git revert` commits referencing the original SHA
2. **Fixes: trailers** — Linux kernel-style `Fixes: <sha>` in commit message
3. **Ticket cross-references** — Same JIRA/Linear/GitHub ticket ID in a `fix:` commit
4. **File overlap** — >50% of a `fix:` commit's source files overlap with the original (excludes docs, configs, lock files)

Both the original change and the fix must be merged to the default branch.
