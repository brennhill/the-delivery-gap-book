# Iteration Budget & Retry Caps

Every agent run has a cost ceiling. If you don't set one, the agent will keep trying — burning tokens, looping through the same failure, and producing increasingly divergent output — until it either stumbles into a solution or hits a platform timeout.

Stripe caps at 2 CI rounds: push, full CI, if it fails the agent gets one retry, if it still fails the task goes to a human. That is the reference implementation. This guide covers why, how, and what to monitor.

---

## Why Caps Matter

### Diminishing returns

Agent iterations follow a steep drop-off curve. The first attempt captures most of the value. The first retry fixes most recoverable failures (typos, missing imports, simple test fixes). By the third attempt, the agent is usually stuck — either the task is poorly scoped, the agent lacks context, or the failure is a flaky test the agent can't control.

Stripe's data supports this: 2 rounds catches the vast majority of recoverable failures. Additional rounds rarely produce better outcomes.

### Unbounded token spend

Each iteration consumes tokens for context loading, reasoning, code generation, and tool calls. A 3-round loop on a complex task can easily consume 5-10x the tokens of a single pass. Without caps, a stuck agent can burn through your daily token budget on a single task.

### Economic Denial of Service (EDoS)

An agent in an infinite retry loop is an EDoS attack on your own budget. This is not theoretical — it happens when agents encounter flaky tests, intermittent network failures, or ambiguous error messages that change between runs. The agent interprets each new error as progress and keeps trying.

---

## The Decision Framework

Match iteration caps to task complexity. Not every task deserves the same budget.

| Task complexity | Iteration cap | Token budget | Example |
|---|---|---|---|
| Simple | 1 round (no retry) | 50K tokens | Fix a typo, update a version number, rename a variable |
| Standard | 2 rounds (Stripe model) | 200K tokens | Implement a well-specified feature, fix a bug with a clear repro |
| Complex | 3 rounds max | 500K tokens | Multi-file refactor, migration with test updates |

### How to classify tasks

- **Simple:** The change is mechanical. A human could describe exactly which lines to change. No judgment required.
- **Standard:** The change requires understanding context and making decisions, but the scope is clear. Most feature work and bug fixes fall here.
- **Complex:** The change touches multiple systems, requires test updates, or involves ambiguous requirements. These tasks should be rare for agents — if most of your agent tasks are "complex," your task decomposition needs work.

### Setting both limits

Always set **both** an iteration cap and a token budget. They catch different failure modes:

- Iteration cap catches retry loops (agent keeps trying the same approach)
- Token budget catches context explosion (agent reads too many files, generates excessive code)

```python
# Example: agent harness configuration
agent_config = {
    "max_iterations": 2,        # Stripe model: push + one retry
    "max_tokens": 200_000,      # Total tokens across all iterations
    "timeout_seconds": 600,     # 10-minute wall clock
    "max_cost_usd": 5.00,       # Hard dollar cap
}
```

---

## What Hitting the Cap Signals

When an agent hits its iteration or token cap, that is data. Do not just increase the cap.

| Signal | Likely cause | Action |
|---|---|---|
| Agent hits iteration cap on first task | Task is too large or poorly scoped | Break the task into smaller pieces |
| Agent hits iteration cap repeatedly on similar tasks | Agent lacks context (missing CLAUDE.md, no architecture docs) | Improve context files |
| Agent hits token cap but not iteration cap | Agent reading too many files or generating verbose output | Narrow the agent's file access scope |
| Agent hits cap on the same test failure | Test is flaky or environment-dependent | Fix the test, don't give the agent more retries |
| Agent hits cap after self-correction attempts | The fix requires understanding the agent doesn't have | Route to human immediately |

### The flaky test trap

Flaky tests are the #1 cause of wasted agent iterations. The agent sees a test fail, changes code to fix it, the test passes (because it was flaky), the agent pushes, a different test flakes, and the cycle continues. If your agent is hitting caps on test failures that you can't reproduce locally, you have a flaky test problem, not an agent problem. Fix the tests.

---

## Stripe's 2-Round Model

Stripe's published approach for AI-generated PRs:

```
Agent generates code and pushes
    → Full CI runs
    → If CI passes → PR ready for review
    → If CI fails → Agent gets CI output, retries once
        → Full CI runs again
        → If CI passes → PR ready for review
        → If CI still fails → Task routed to human
```

This is deliberately conservative. Stripe's reasoning: the cost of a stuck agent burning tokens for 30 minutes far exceeds the cost of routing one task to a human. The 2-round cap is a business decision, not a technical limitation.

---

## Implementation

### Agent harness configuration

```python
class IterationBudget:
    """Enforce iteration and token caps on agent runs."""
    
    def __init__(self, max_iterations=2, max_tokens=200_000, max_cost_usd=5.0):
        self.max_iterations = max_iterations
        self.max_tokens = max_tokens
        self.max_cost_usd = max_cost_usd
        self.current_iteration = 0
        self.tokens_used = 0
        self.cost_usd = 0.0
    
    def can_continue(self) -> bool:
        if self.current_iteration >= self.max_iterations:
            return False
        if self.tokens_used >= self.max_tokens:
            return False
        if self.cost_usd >= self.max_cost_usd:
            return False
        return True
    
    def record_iteration(self, tokens: int, cost: float):
        self.current_iteration += 1
        self.tokens_used += tokens
        self.cost_usd += cost
    
    def reason_for_stop(self) -> str:
        if self.current_iteration >= self.max_iterations:
            return f"Iteration cap reached ({self.max_iterations} rounds)"
        if self.tokens_used >= self.max_tokens:
            return f"Token budget exhausted ({self.tokens_used:,} / {self.max_tokens:,})"
        if self.cost_usd >= self.max_cost_usd:
            return f"Cost ceiling hit (${self.cost_usd:.2f} / ${self.max_cost_usd:.2f})"
        return "Unknown"


def run_agent_task(task, budget: IterationBudget):
    """Run an agent task with budget enforcement."""
    
    while budget.can_continue():
        # Agent generates code
        result = agent.execute(task)
        budget.record_iteration(result.tokens_used, result.cost)
        
        # Run CI
        ci_result = run_ci()
        
        if ci_result.passed:
            return AgentResult(status="success", iterations=budget.current_iteration)
        
        if not budget.can_continue():
            break
        
        # Feed CI output back to agent for retry
        task.add_context(f"CI failed. Output:\n{ci_result.output}\nFix the failures.")
    
    # Budget exhausted — route to human
    return AgentResult(
        status="escalated",
        reason=budget.reason_for_stop(),
        iterations=budget.current_iteration,
        ci_output=ci_result.output,
    )
```

### SDK-level caps

Most agent SDKs have built-in budget parameters. Set these as a safety net even if you have application-level caps:

| SDK | Parameter | Recommended starting value |
|---|---|---|
| OpenAI Agents SDK | `max_turns` | 10 |
| LangGraph | `recursion_limit` | 15 |
| CrewAI | `max_iter` + `max_execution_time` | 15 iterations, 600s |
| Anthropic | `budget_tokens` (thinking) | 100K |

These are per-invocation limits within a single iteration. Your application-level iteration cap wraps around these — they are independent controls.

---

## Monitoring

Track these metrics weekly. Trends are more important than absolute numbers.

| Metric | What it tells you | Alert threshold |
|---|---|---|
| Cap hit rate | % of tasks that exhaust their iteration budget | Rising over 2 consecutive weeks |
| First-pass success rate | % of tasks that pass CI on first attempt | Falling below 60% |
| Retry success rate | % of retried tasks that pass on second attempt | Falling below 40% |
| Mean tokens per task | Average token consumption across all tasks | Rising over 2 consecutive weeks |
| Escalation rate | % of tasks routed to humans due to cap exhaustion | Rising over baseline |

### What the trends mean

**Rising cap hit rate:** Prompts are getting worse, task scoping is degrading, or test reliability has dropped. Investigate the specific tasks hitting caps — you'll usually find a pattern (same repo, same test suite, same type of change).

**Falling first-pass success rate:** Agent context may be stale (CLAUDE.md out of date), or the codebase has changed in ways the agent can't navigate. Update context files and check whether recent architectural changes have invalidated the agent's assumptions.

**Rising escalation rate:** The agent is being asked to do things it can't do. Review the escalated tasks. If they're genuinely hard, that's fine — route them to humans. If they're tasks the agent should handle, the agent's configuration or context needs attention.

### Dashboard query (pseudocode)

```sql
-- Weekly iteration budget report
SELECT
    DATE_TRUNC('week', created_at) AS week,
    COUNT(*) AS total_tasks,
    AVG(iterations_used) AS avg_iterations,
    AVG(tokens_used) AS avg_tokens,
    SUM(CASE WHEN status = 'success' AND iterations_used = 1 THEN 1 ELSE 0 END)::float 
        / COUNT(*) AS first_pass_rate,
    SUM(CASE WHEN status = 'escalated' THEN 1 ELSE 0 END)::float 
        / COUNT(*) AS escalation_rate
FROM agent_runs
GROUP BY 1
ORDER BY 1 DESC;
```

---

## Common Mistakes

**Mistake: Setting generous caps "to be safe."** A 10-round cap is not safer than a 2-round cap. It just means the agent burns 5x the tokens before you find out the task was impossible. Start tight, loosen based on data.

**Mistake: Increasing caps instead of fixing root causes.** If agents keep hitting the 2-round cap, the answer is almost never "give them 4 rounds." The answer is better prompts, better context, or smaller tasks.

**Mistake: No cap on token spend.** Iteration caps without token caps leave a gap. An agent can do enormous work in a single iteration — reading hundreds of files, generating thousands of lines — and blow your budget without triggering the iteration limit.

**Mistake: Treating all tasks the same.** A version bump does not need the same budget as a feature implementation. Classify tasks and set caps accordingly. If your harness doesn't support per-task caps, default to the standard (2 rounds) and only override for explicitly complex tasks.
