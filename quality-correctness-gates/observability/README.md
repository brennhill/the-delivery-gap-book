# Observability — The Meta-Requirement

Without observability, you cannot tell whether any other control is working. Gates can be inert. Scope can be violated daily. Costs can climb for months. Reviewers can rubber-stamp every PR. If you are not watching, the dashboard is green and the organization believes the system is working.

This guide covers pipeline observability — are your gates actually catching anything? For agent observability, see [../agent-monitoring/](../agent-monitoring/). For delivery metrics, see `measurement-guidance/`.

---

## Are Your Gates Working?

Gates that never fire are either perfectly placed or completely broken. Most teams build gates once and never check whether they catch anything.

### What to track

| Signal | What it tells you | Healthy | Broken |
|--------|------------------|---------|--------|
| Gate failure rate per tier | Are gates catching real problems? | Nonzero failure rate — PRs regularly fail at least one check | 0% failure rate across a full quarter |
| Time from PR open to first gate result | Are gates fast enough to be useful? | < 5 minutes for Tier 0, < 15 for Tier 1 | > 30 minutes (developers stop waiting) |
| Gate override rate | Are people bypassing controls? | < 5% of failures are overridden | > 20% overridden, or no tracking at all |
| False positive rate | Are gates crying wolf? | < 10% of failures are false positives | > 30% (developers learn to ignore) |

### How to instrument

Most CI platforms expose this data. The implementation is usually a post-pipeline script that queries your CI API and writes to a dashboard or CSV.

**GitHub Actions:** Use the [GitHub Actions API](https://docs.github.com/en/rest/actions) to query workflow run conclusions. Filter by job name to isolate gate results.

**GitLab CI:** Use the [Pipelines API](https://docs.gitlab.com/ee/api/pipelines.html) to pull job-level pass/fail data.

**SonarQube/SonarCloud:** The [Quality Gates API](https://docs.sonarqube.org/latest/project-administration/webhooks/) provides per-project gate status. Enable webhooks for real-time tracking.

### Quarterly gate audit

Print this table. Walk each tier with your tech lead. Ask: "Is this gate catching real problems, or has it become inert?"

```
Tier 0 (Static Analysis):  Last failure date: ___  Failure rate this quarter: ___%
Tier 1 (Contract Gates):   Last failure date: ___  Failure rate this quarter: ___%
Tier 2 (Invariant Gates):  Last failure date: ___  Failure rate this quarter: ___%
Tier 3 (Policy Gates):     Last failure date: ___  Failure rate this quarter: ___%
Tier 4 (Behavioral Gates): Last failure date: ___  Failure rate this quarter: ___%
```

A gate with zero failures for an entire quarter is almost certainly not checking anything meaningful. Tighten rules, add AI-specific checks, or investigate whether the gate is running at all.

---

## Trend Detection

A single bad week is noise. Two consecutive weeks moving in the wrong direction is signal. Flag any metric that moves > 15% in the wrong direction for two consecutive weeks.

---

## OpenTelemetry for AI

The OpenTelemetry project has published semantic conventions for generative AI observability. These provide standard attribute names for model calls, token usage, and tool invocations across providers.

- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-metrics/)

If you are building custom observability infrastructure, adopt these conventions. They ensure your traces are compatible with the growing ecosystem of AI observability tools.

---

## Further Reading

- [OpenAI: How we monitor internal coding agents for misalignment](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/) — The most detailed public guide on agent behavioral monitoring
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Production monitoring + automated evals + human review
- [DORA: Software delivery performance metrics](https://dora.dev/guides/dora-metrics/) — The industry standard for delivery measurement
