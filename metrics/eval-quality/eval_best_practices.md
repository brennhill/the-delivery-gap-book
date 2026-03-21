# Eval Quality Best Practices

Eval quality answers one question: are defects being caught early enough, and are machines absorbing enough of the verification load?

## The four eval metrics

### Machine catch rate

`machine_catches / (machine_catches + human_catches)`

Target: above 50%. If humans are catching more than machines, your gates are underbuilt and your most expensive people are doing a machine's job.

How to improve:
- Add a gate tier you're missing (see the gate tooling by language)
- Make warning-only gates blocking
- Add AI code review (CodeRabbit, Anthropic Code Review, or the multi-pass review script)

### Reviewer-minutes per accepted change

`total_reviewer_minutes / accepted_changes`

Watch the trend, not the absolute number. If this is rising, your review layer is being overwhelmed by volume. If it's falling, your gates are absorbing more of the load.

Warning threshold: if median review exceeds 60 minutes, the SmartBear/Cisco research says effectiveness has already collapsed.

### Defect escape rate

`production_defects / (production_defects + pre_production_defects)`

Target: below 15%. Above 30% means most bugs are reaching production — your gates are not catching enough.

Requires issue tracker integration or manual labeling:
- Label bugs with where they were found: "production" or "found-in-review" / "found-in-ci"
- Count each bug once using first-finder-wins

What NOT to count as defects: style comments, formatting nits, flaky CI timeouts, duplicate findings.

### Change fail rate (DORA)

`failed_deployments / total_deployments`

DORA benchmarks:
- Elite: < 5%
- High: 5-10%
- Medium: 10-15%
- Low: > 15%

## Step 0: Error analysis before gate building

Before adding gates, look at what actually fails. Most teams skip this and build gates based on what they *think* will go wrong. The result: gates that catch theoretical problems while real failures slip through.

1. **Collect 50-100 real outputs** — random sample from the last 1-2 weeks, not cherry-picked
2. **Categorize failures manually** — let categories emerge from the data, don't use predefined lists
3. **Prioritize by frequency × severity** — your top 3-5 categories become your first gates
4. **Build one eval per failure mode** — targeted pass/fail checks, not generic quality scores

See [tools/eval-examples/error-analysis-workflow/](../../tools/eval-examples/error-analysis-workflow/) for runnable scripts that automate the collection and summarization steps.

Generic metrics (ROUGE, BERTScore, "similarity score") are the eval equivalent of measuring PR volume instead of accepted outcomes. They optimize a proxy, not the thing you care about. Domain-specific evals targeting your actual failure modes are what move the machine catch rate.

## Building gates that actually work

### Gates must block, not warn

A gate that logs a warning but doesn't fail the build is not a gate. It's a suggestion. Engineers will train themselves to ignore it within weeks.

### Audit quarterly

A gate that never fires is either perfectly placed or completely broken. Run the audit table from the Quality Gates chapter every quarter. If a tier scores "healthy" but your defect escape rate is rising, your audit criteria are wrong.

### The three invariant questions

Before shipping any feature, ask:
1. What must never happen twice?
2. What must always be true after this operation completes?
3. What breaks if operations run out of order?

If the answers are clear, they define your invariant tests. If they're not clear, the feature may not be understood well enough to ship safely.

## Official provider guides

- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Production monitoring + automated evals + human review as a combined approach. Drift detection post-launch.
- [Anthropic: Building Effective AI Agents](https://resources.anthropic.com/building-effective-ai-agents) — End-to-end agent patterns with eval guidance.

## Research basis

- SmartBear/Cisco: 2,500 reviews, 3.2M lines. 70-90% defect discovery at 200-400 lines. Effectiveness collapses after 60 minutes.
- CodeRabbit: AI-authored code carries 1.7x more issues than human-authored code
- DORA: change fail rate and deployment rework rate as core delivery metrics
- CodeX-Verify (arXiv 2511.16708): multi-perspective review improves accuracy from 32.8% to 72.4%
