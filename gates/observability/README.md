# Observability — The Meta-Requirement

Without observability, you cannot tell whether any other control is working. Gates can be inert. Scope can be violated daily. Costs can climb for months. Reviewers can rubber-stamp every PR. If you are not watching, the dashboard is green and the organization believes the system is working.

The book calls this "missing observability" — the breakdown that makes all other breakdowns invisible.

This guide covers three layers of observability for AI-assisted and agentic development. Each layer is independent. Start wherever your biggest gap is.

---

## Layer 1: Pipeline Observability — Are Your Gates Working?

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

## Layer 2: Delivery Observability — Is the System Improving?

Pipeline observability tells you whether gates work. Delivery observability tells you whether the whole system is producing trusted changes at sustainable cost.

### The four-number scorecard

Track weekly. Review in a 15-minute meeting with EM, tech lead, and one rotating IC.

| Metric | Source | How to compute |
|--------|--------|---------------|
| **Cost per accepted change** | Cost calculator + git history | See [metrics/cost-per-accepted-change/](../../metrics/cost-per-accepted-change/) |
| **Rework rate** | Git history | See [metrics/rework-detection/](../../metrics/rework-detection/) |
| **Reviewer-minutes per accepted change** | GitHub/GitLab review timestamps | See [metrics/eval-quality/](../../metrics/eval-quality/) |
| **Defect escape rate** | Issue tracker + CI data | Production bugs / total bugs found |

### Trend detection

A single bad week is noise. Two consecutive weeks moving in the wrong direction is signal. Flag any metric that moves > 15% in the wrong direction for two consecutive weeks.

### Tools for delivery observability

| Tool | What it does | URL |
|------|-------------|-----|
| LinearB | DORA metrics, cycle time, PR analytics | https://linearb.io |
| Sleuth | DORA metrics, deploy tracking, change failure rate | https://sleuth.io |
| Swarmia | Engineering effectiveness, investment balance | https://swarmia.com |
| Faros AI | Engineering intelligence, 50+ data sources | https://faros.ai |

If you do not want a platform, a spreadsheet and git history are sufficient. The scripts in `metrics/` produce the numbers. The cadence matters more than the tooling.

---

## Layer 3: Agent Observability — What Are Your Agents Doing?

This is the layer most teams are missing entirely. Traditional monitoring catches errors. Agent monitoring catches behavior — an agent that succeeds through the wrong path is invisible to error-based monitoring.

### The full guide

See **[../agent-monitoring/](../agent-monitoring/)** for the complete implementation path:

1. **Capture structured traces** — every tool call, file access, API request (Langfuse, Arize Phoenix, LangSmith)
2. **Build behavioral baselines** — what "normal" looks like across 50-100 sessions
3. **Set alert thresholds** — 3x p95 on file reads, 5x median on token usage, any new tool call
4. **LLM-as-judge sampling** — 5-10% of sessions reviewed by a separate model
5. **Production monitoring signals** — extended golden signals for AI systems
6. **Track iteration budget per run** — tokens, turns, cost per task

### Per-run cost tracking tools

| Tool | What it tracks | URL |
|------|---------------|-----|
| Stripe `@stripe/token-meter` | Per-call cost across OpenAI, Anthropic, Gemini | https://github.com/stripe/ai |
| LangSmith | Token usage, latency, cost breakdowns per trace | https://smith.langchain.com |
| AgentOps | Session-level cost tracking, 400+ LLMs | https://github.com/AgentOps-AI/agentops |
| Langfuse | Token and cost tracking per trace/span | https://langfuse.com |
| Honeycomb | Usage monitoring at minute-level granularity | https://docs.honeycomb.io |

### SDK budget parameters

Every major agent SDK has a built-in cap to prevent runaway execution:

| SDK / Platform | Parameter | Default |
|---|---|---|
| OpenAI Agents SDK | `max_turns` | 10 |
| LangGraph | `recursion_limit` | 25 |
| CrewAI | `max_iter` + `max_execution_time` | 25 iterations |
| Anthropic | `budget_tokens` (thinking) | varies |
| Azure AI Gateway | `llm-token-limit` policy | per-project |

Set hard limits on at least two dimensions per agent run: turn limit + token budget, or token budget + wall-clock timeout.

---

## The Observability Stack at a Glance

```
Layer 3: Agent Observability
  ├── Structured traces (Langfuse, Phoenix, LangSmith)
  ├── Behavioral baselines + alert thresholds
  ├── LLM-as-judge sampling
  └── Per-run cost tracking (Stripe token-meter, AgentOps)

Layer 2: Delivery Observability
  ├── Four-number weekly scorecard
  ├── Trend detection (2-week signal threshold)
  └── Engineering intelligence platform or spreadsheet

Layer 1: Pipeline Observability
  ├── Gate failure rates per tier
  ├── Override and false positive tracking
  └── Quarterly gate audit
```

Start from the bottom. If your gates are not instrumented, you cannot trust your delivery metrics. If your delivery metrics are not tracked, you cannot tell whether agents are helping or hurting.

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
- [Stripe: A framework for pricing AI products](https://stripe.com/blog/a-framework-for-pricing-ai-products) — Cost tracking and billing infrastructure for AI
