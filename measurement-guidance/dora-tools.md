# Established Tools for Delivery Measurement

You don't need to build measurement infrastructure from scratch. These tools exist, they work, and they've been validated across thousands of engineering organizations.

Start with the free options. Move to commercial tools when you need cross-team visibility or deeper analysis.

> We are not affiliated with any of these tools. This list reflects what's available as of early 2026. Evaluate based on your stack and needs.

---

## Free / Open Source

### Four Keys (Google)

Open-source DORA metrics dashboard built by the Google DORA team themselves. Ingests data from GitHub, GitLab, and CI/CD systems to calculate the four key DORA metrics.

- **Pricing:** Free, open source
- **Best at:** Pure DORA metric calculation with minimal setup
- **Note:** Requires BigQuery. Best suited for teams already on GCP.

### Apache DevLake

Open-source dev data platform that connects to GitHub, GitLab, Jira, Jenkins, and more. Calculates DORA metrics out of the box with a Grafana dashboard.

- **Pricing:** Free, open source (Apache 2.0)
- **Best at:** Pulling data from multiple tools into a single view. Most flexible open-source option.

### GitHub CLI (`gh`)

GitHub's own CLI can extract PR data, review times, CI status, and more. Not a dashboard, but a powerful way to pull raw data for teams that want to build lightweight reports.

- **Pricing:** Free
- **Best at:** Quick queries and ad-hoc analysis without installing anything new. See [GitHub Actions Reporting](github-actions-reporting.md) for practical examples.

---

## Commercial (Worth Evaluating)

### Swarmia

Engineering metrics platform with DORA metrics, investment balance tracking, and working agreement monitoring. Good integration with Jira and Linear.

- **Pricing:** Paid (per-developer pricing, free tier for small teams)
- **Best at:** Team-level visibility and connecting engineering metrics to business outcomes.

### LinearB

Cycle time analytics with breakdown into coding time, pickup time, review time, and deploy time. Correlates metrics with specific workflow bottlenecks.

- **Pricing:** Freemium (free for small teams, paid for advanced features)
- **Best at:** Understanding where time goes in your development cycle.

### Sleuth

DORA-focused platform built around deployment tracking. Tracks change fail rate, deploy frequency, lead time, and MTTR with strong CI/CD integration.

- **Pricing:** Freemium (free for one project, paid for more)
- **Best at:** Teams that want DORA metrics specifically and already have deployment pipelines instrumented.

### DX (formerly DX by Abi Noda)

Combines developer surveys with DORA metrics and the SPACE framework. Measures developer experience alongside delivery metrics.

- **Pricing:** Paid (enterprise pricing)
- **Best at:** Organizations that want to understand both delivery performance and developer satisfaction together.

### Faros AI

Comprehensive engineering intelligence platform that ingests data from 50+ tools. Tracks DORA, SPACE, and AI-specific metrics.

- **Pricing:** Paid (enterprise pricing)
- **Best at:** Large organizations with complex toolchains that need a single pane of glass across many teams and tools.

### GitClear

Code churn analysis and AI-generated code detection. Tracks lines of code moved, deleted, and rewritten — not just added.

- **Pricing:** Freemium (free for public repos, paid for private)
- **Best at:** Understanding code quality trends and identifying AI-generated code patterns across your codebase.

### CodeScene

Behavioral code analysis that identifies hotspots, technical debt, and team coordination patterns from git history.

- **Pricing:** Freemium (free for open source, paid for private repos)
- **Best at:** Identifying which parts of your codebase are accumulating risk and where team coordination is breaking down.

---

## How to Choose

**If you're just starting:** Use the `gh` CLI and your existing GitHub/CI dashboards. That's enough for a [weekly review](weekly-review-guide.md).

**If you want DORA metrics without spending money:** Apache DevLake is the most flexible open-source option. Four Keys is simpler but requires GCP.

**If you're ready to invest:** Pick one commercial tool, run a pilot with one team for a month, and see if the insights change any decisions. If they don't, you don't need it yet.

**If executives are asking for AI-specific metrics:** Faros AI and GitClear are the furthest along in tracking AI adoption patterns. But be honest about what the metrics can and can't tell you — detecting AI involvement in code is still an imprecise science.
