# What to Measure (and What Not To)

You're under pressure to show that AI adoption is working. Dashboards, OKRs, executive summaries. The temptation is to measure everything and present a score.

Don't. The only question that matters is: **are things better, worse, or the same as last week?**

Here's what's worth tracking, organized by how hard it is to get.

> **What we deliberately don't provide:** Custom measurement scripts. Our research found that automated metrics from git history alone are unreliable across different repo types and review cultures. Rather than ship tools that create false confidence, we point you to established platforms that have solved this properly.

---

## Easy: Available from Git/GitHub Alone

These require nothing beyond your existing GitHub setup.

### PR Volume and Trend

What it tells you: Whether your team's throughput is changing over time — and in which direction.
Where to get it: GitHub Insights (pulse tab), or `gh pr list --state merged --search "merged:>2024-01-01"`.

### PR Size Distribution (% Over 400 Lines)

What it tells you: Large PRs get worse reviews — the relationship is well-documented. If your percentage of oversized PRs is growing, review quality is probably declining.
Where to get it: GitHub PR list shows additions/deletions per PR. Most engineering analytics tools surface this automatically.

### Time to First Review

What it tells you: How long PRs sit before anyone looks at them. Long wait times compress actual review time and encourage rubber-stamping.
Where to get it: GitHub shows review timestamps on each PR. The `gh` CLI can extract this: `gh pr list --state merged --json number,createdAt,reviews`.

### Time to Merge

What it tells you: Total cycle time from PR open to merge. Rising merge times may indicate process friction or review bottlenecks.
Where to get it: Same as above — `gh pr list --state merged --json number,createdAt,mergedAt`.

### Bot vs Human Review Ratio

What it tells you: Whether automated tooling (linters, security scanners, AI review bots) is supplementing or replacing human review.
Where to get it: GitHub shows which reviews came from bot accounts. Filter review authors by `[bot]` suffix.

### Rubber-Stamp Rate

What it tells you: The percentage of PRs approved in under 5 minutes with no review comments. This is a proxy for review quality — not proof of a problem, but a signal worth watching.
Where to get it: Compare review timestamp to approval timestamp and check comment count. Most engineering analytics platforms calculate this automatically.

---

## Moderate: Requires CI Integration

These need your CI pipeline (GitHub Actions, CircleCI, etc.) connected to your workflow.

### CI Gate Pass/Fail Rate

What it tells you: How often automated checks catch problems before merge. This is the closest you'll get to a "machine catch rate" without dedicated tooling.
Where to get it: GitHub Actions dashboard shows pass/fail rates. See [GitHub Actions Reporting](github-actions-reporting.md) for practical steps.

### Build Success Rate

What it tells you: Whether your main branch stays green. A declining build success rate often means PRs are getting merged without adequate automated validation.
Where to get it: Your CI provider's dashboard. GitHub Actions shows this under the Actions tab for each workflow.

---

## Hard: Requires Ecosystem Tooling (Jira/Linear + CI/CD + Observability)

These are the DORA metrics and their relatives. They're the most valuable measures of delivery health, but they require connecting multiple systems — your issue tracker, CI/CD pipeline, deployment tooling, and incident management.

### Change Fail Rate

What it tells you: What percentage of deployments cause a failure requiring remediation. The single best indicator of whether your quality gates are working.
Where to get it: Requires linking deployments to incidents. DORA tools like Four Keys or Sleuth automate this.

### Deployment Frequency

What it tells you: How often you ship to production. More frequent deployment usually correlates with smaller batch sizes and faster feedback.
Where to get it: Your deployment pipeline. Most DORA platforms pull this from CI/CD events.

### Lead Time for Changes

What it tells you: Time from commit to production. Captures the full pipeline, not just the PR review portion.
Where to get it: Requires linking commits to deployments. This is what DORA tooling was built for.

### Change Failure Rate

What it tells you: What percentage of deployments cause production degradation requiring remediation. This is a DORA core metric — most teams already have tooling for it.
Where to get it: Requires linking deployments to incidents, rollbacks, or hotfixes. DORA tools like Four Keys or Sleuth automate this. Also track non-degrading escapes (defects that reach production without causing service degradation) separately — each one is a gating opportunity your pipeline should have caught.

---

## The Honest Truth About Measurement

The easy metrics are easy because they're shallow. PR volume tells you something, but not the thing you actually care about (did we ship working software?).

The hard metrics are hard because they require connecting systems that most organizations haven't connected. But they're the ones that answer the questions executives are actually asking.

**Start with what you have.** If all you can measure today is PR count and CI pass rate, that's enough to run a meaningful [weekly review](weekly-review-guide.md). You can invest in deeper measurement as the practice matures.

The cadence of looking at your metrics matters more than the sophistication of those metrics.
