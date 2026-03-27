# The Five-Metric Diagnostic

Five categories tell you whether your control infrastructure has kept pace with your generation velocity. Each category has a code-side metric and an agent-side metric — ten sub-metrics total.

The **four-number scorecard** (cost per accepted change, change failure rate, reviewer-minutes per accepted change, rework rate) is the starting subset. Instrument those in Week 1. The full diagnostic below is the destination.

---

## The Diagnostic

| # | What you are measuring | For code | For agents |
|---|---|---|---|
| 1 | **Output trust** | Rework rate | Judge veto rate |
| 2 | **Gate effectiveness** | Machine catch rate | Deterministic pass rate |
| 3 | **Human sustainability** | Reviewer-minutes per accepted change | Human turns per session |
| 4 | **Scope control** | Change failure rate | Scope violation rate |
| 5 | **Unit cost** | Cost per accepted change | Iteration budget per run |

---

## Each Metric Explained

### 1. Output Trust

**Rework rate (code).** What percentage of merged changes required significant rework — not just bug fixes, but changes where the approach was wrong, the intent was misunderstood, or the design had to be reconsidered. Rework does not have to escape to production; catching it in review still counts. This is an intent clarity signal: high rework means insufficient upfront thinking.

**Judge veto rate (agents).** A second AI reviews the first AI's work. When an agent completes a task, a separate LLM evaluates the output against the original spec and vetoes sessions where the agent drifted, over-reached, or produced something that does not match what was asked for. A healthy veto rate means the system is checking itself.

### 2. Gate Effectiveness

**Machine catch rate (code).** Of all defects found before production, what percentage were caught by automated gates versus discovered by human reviewers? If humans are still catching most of the issues, your automated verification is underbuilt and your most expensive people are doing work the pipeline should absorb.

**Deterministic pass rate (agents).** What percentage of agent outputs pass all automated checks before reaching a human for review? If the pass rate is low, the agent is generating low-quality work. If it is 100%, either the agent is excellent or the checks are too lenient.

### 3. Human Sustainability

**Reviewer-minutes per accepted change (code).** How long does a human spend reviewing each change that actually makes it to production? If this number is rising, your review layer is being overwhelmed by volume. This is the most direct measure of whether verification is scaling with generation.

**Human turns per session (agents).** How many times does a human intervene during an agent session? Declining means the agent is gaining autonomy. Rising means it needs more hand-holding. Either direction is a signal worth tracking.

### 4. Scope Control

**Change failure rate (code).** What percentage of your deployments cause production degradation requiring remediation — rollbacks, hotfixes, or corrective action. This is a DORA core metric, and most teams already have tooling for it. Also track non-degrading escapes separately: defects that reach production without causing service degradation. Each one is a gating opportunity.

**Scope violation rate (agents).** How often does an agent attempt actions outside its documented scope? This requires logging attempted actions, not just successful ones. An agent that tries to call a forbidden tool and gets blocked is a working constraint.

### 5. Unit Cost

**Cost per accepted change (code).** The total cost of delivering a change that survived review, passed evaluation, reached production, and stayed there. Includes model cost, infrastructure, human review time, and rework. This is the number your CFO can evaluate.

**Iteration budget per run (agents).** The token ceiling, maximum retries, and compute cost allocated per agent task. If the agent regularly hits its ceiling, the tasks are too complex or the agent is looping.

---

## How Companies Track These

No company publishes exact numbers for all ten sub-metrics. Each tracks versions of the first four categories demonstrably. Unit cost is the gap — every company tracks cost proxies, but none publishes the full unit economic that "cost per accepted change" requires. This is why we propose it as a unified metric.

### What they demonstrably track

| Category | Stripe | Spotify | Uber | Anthropic |
|---|---|---|---|---|
| **Output trust** | Human review on every PR | LLM-as-judge vetoes ~25% of sessions | 75% usefulness rating, 65% of comments addressed | 67% more merged PRs/engineer |
| **Gate effectiveness** | Sandboxed devboxes; deterministic gates interleaved with agent steps | Deterministic verifiers block PRs on failure | uReview analyzes 90% of 65K weekly diffs | Substantive review comments 16%→54% |
| **Human sustainability** | 1,300+ PRs/week, all human-reviewed | Engineers shifted from writing code to designing verification loops | 1,500 developer hours saved weekly | Code Review on nearly every internal PR |
| **Scope control** | Scope enforcement built into blueprint architecture | Sandboxed containers, limited permissions and binaries | Validator flags security vulnerabilities in real time | Not publicly documented |

Sources: Stripe Minions blog (2026), Spotify Honk blog series (2025), Uber uReview blog (2025) / Pragmatic Engineer (2026), Anthropic internal report (2025) / Code Review launch (2026).

### What they track for unit cost (proxies, not the full picture)

| Company | What they publish | What's missing |
|---|---|---|
| **Stripe** | Max 2 CI rounds per minion run (engineering constraint) | No cost-per-change, no dollar figures |
| **Spotify** | 60-90% time savings for migrations; session-level success/veto tracking | No cost-per-change, no dollar figures |
| **Anthropic** | $6/dev/day average, $25 max per agent job | Input cost only — no denominator for accepted output |
| **Uber** | 1,500 dev hours saved/week; "AI costs up 6x since 2024" | Review time saved, not cost per delivered output |

Every company measures some version of what it costs to run AI. None of them connects that cost to the denominator that matters: accepted changes that survived review, passed evaluation, reached production, and stayed there. They track fuel cost without tracking cost per mile.

**This is why the book proposes cost per accepted change as a unified metric.** It combines what these companies measure separately — compute spend, human review time, rework cost, infrastructure cost — into a single unit economic that a CFO can evaluate. The metric is a synthesis, not an industry standard. No company has publicly connected these dots yet. But the components are all being tracked; the connection is what's missing.

---

## Mapping to the Four-Number Scorecard

The four-number scorecard is the starting subset of the five-metric diagnostic. It covers the code side of four of the five categories:

| Scorecard metric | Diagnostic category |
|---|---|
| Cost per accepted change | Unit cost |
| Change failure rate | Scope control |
| Reviewer-minutes per accepted change | Human sustainability |
| Rework rate | Output trust |

**What's missing from the scorecard:** Gate effectiveness (machine catch rate / deterministic pass rate). Add this once your gate failures and review findings share a schema — it requires knowing which defects were caught by machines versus humans.

**What the scorecard doesn't cover:** Agent-side metrics. If you are running autonomous agents in production, extend to the full diagnostic. The agent-side metrics (judge veto rate, deterministic pass rate, human turns per session, scope violation rate, iteration budget per run) are the controls that prevent the agent from compounding errors unsupervised.

---

## Reading the Diagnostic

If all five categories are stable or improving, your control infrastructure is scaling with your generation velocity.

**Output trust degrading** (rework or veto rate climbing): the quality entering your pipeline is declining. The fix is better specs and tighter task scoping upstream.

**Gate effectiveness low** (machine catch rate below 50% or deterministic pass rate low): your automated verification is underbuilt. Add deterministic gates before asking humans to review more.

**Human sustainability declining** (reviewer-minutes rising, human turns rising): your verification layer is being overwhelmed. Either automate more of the verification load or reduce generation velocity until capacity catches up.

**Scope control failing** (change failure rate or scope violation rate rising): changes or agents are acting outside intended boundaries. Tighten permissions, add containment, review the tier classification.

**Unit cost rising** (cost per accepted change climbing, iteration budgets exceeded): use the diagnostic to find which category is driving the cost — it is almost never the token spend alone.
