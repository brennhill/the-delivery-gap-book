# How to See What Your CI Caught (GitHub Actions)

Your CI pipeline catches problems before they reach production. Here's how to see what it's catching, using GitHub's built-in tools.

---

## View Failed Checks on Merged PRs (GitHub UI)

1. Go to your repository on GitHub
2. Click **Pull requests** > **Closed**
3. Open any merged PR
4. Scroll to the **Checks** section at the bottom
5. Failed checks show with a red X — click to see details

This shows you what CI flagged on PRs that eventually merged. If a PR has multiple check runs, it means the author had to fix something before the PR was mergeable. That's your CI doing its job.

---

## Query Check Failures with `gh` CLI

List recent failed workflow runs:

```bash
gh run list --status failure --limit 20
```

List failed runs for a specific workflow:

```bash
gh run list --workflow "ci.yml" --status failure --limit 20
```

See failure details for a specific run:

```bash
gh run view <run-id> --log-failed
```

Count failures over the past week:

```bash
gh run list --status failure --created ">$(date -v-7d +%Y-%m-%d)" --json conclusion --jq 'length'
```

Compare to total runs for a pass rate:

```bash
gh run list --created ">$(date -v-7d +%Y-%m-%d)" --json conclusion --jq 'length'
```

---

## Add a Summary Step to Your Workflow

If you want a quick count of how often your gates catch issues, add a step at the end of your CI workflow that logs the outcome. This isn't a custom metrics tool — it's just making your existing CI results easier to find.

```yaml
- name: Report gate outcome
  if: always()
  run: |
    echo "### CI Gate Summary" >> $GITHUB_STEP_SUMMARY
    echo "- **Result:** ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
    echo "- **PR:** #${{ github.event.pull_request.number }}" >> $GITHUB_STEP_SUMMARY
    echo "- **Trigger:** ${{ github.event_name }}" >> $GITHUB_STEP_SUMMARY
```

This writes to GitHub's job summary, visible in the Actions tab for each run. Over time, it gives you a browsable record of what your gates caught.

---

## What This Tells You (and What It Doesn't)

**What you can see:** How often CI catches lint errors, test failures, type errors, security issues, and other automated checks before code merges.

**What you can't see from CI alone:**
- What developers caught locally before pushing (the biggest filter, invisible to you)
- What human reviewers caught in code review (visible in PR comments, but hard to quantify)
- What escaped to production despite passing CI (requires incident tracking)

CI catch data is a **floor**, not a ceiling. Your actual defect catch rate is higher than what CI shows — you just can't measure the rest without additional tooling.

This is still valuable. If your CI failure rate drops to near zero, it either means your code quality is excellent or your gates aren't testing enough. Both are worth investigating.
