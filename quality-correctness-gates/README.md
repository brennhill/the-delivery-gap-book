# Quality-Correctness Gates — The Quality Gate Tiers

The Verification Triangle tells you what to measure. Gates are what make the eval quality vertex strong. Without gates, the weekly review is reading gauges on a pipeline with no valves.

Six tiers of verification, each catching a failure class the tier below cannot see. The tiers are cumulative — you should not skip to Tier 3 without Tier 0. Five machine tiers handle what can be automated. Tier 5 — human review — handles what cannot.

---

## The Six Tiers

### Tier 0 — Static Analysis

Linting, type checking, secret detection, PR size limits. Catches the cheapest failures before any human sees the code. Everything runs in CI, everything blocks on failure.

Critical: enforce a 400-line PR size limit. The SmartBear/Cisco study (2,500 reviews, 3.2M lines) found defect detection collapses above 400 lines. PRs over 1,000 lines show 70% lower detection rates. If AI generated the oversized PR, AI should split it.

**GitHub Actions:**
```yaml
- name: Check PR size
  run: |
    LINES=$(gh pr diff ${{ github.event.pull_request.number }} | wc -l)
    if [ "$LINES" -gt 400 ]; then
      echo "::error::PR is $LINES lines. Max 400. Please split."
      exit 1
    fi
```

**GitLab CI:**
```yaml
check-pr-size:
  script:
    - LINES=$(git diff origin/main...HEAD | wc -l)
    - if [ "$LINES" -gt 400 ]; then echo "PR too large ($LINES lines). Split it."; exit 1; fi
```

**Who does this in production:**
- **Stripe:** Deterministic lint node in blueprint runs before any push. Background daemon precomputes lint heuristics with sub-second cached results. If it will fail CI, enforce it immediately.
- **Webflow:** Standard CI gates on every PR — AI code held to the same standard as human code, no exceptions.

### Tier 1 — Contract Gates

API contract checks: does the interface behave as documented? Schema validation on all AI-generated outputs. Catches silent breakage between services — the failure that shows up three weeks later when nobody remembers what changed.

**MCP verify tool pattern:** Spotify's Honk system exposes a generic `verify` MCP tool that agents call after every code change. The agent doesn't need to know the build system, test runner, or linting config — it calls `verify`, which hides all that complexity behind a single interface. This is the right abstraction: the agent asks "did I break anything?" and the tool answers definitively. Build your contract gates so agents can invoke them without understanding your CI topology.

**Who does this in production:**
- **Spotify:** Independent verifiers activate automatically based on component contents (e.g., Maven verifier fires when it finds `pom.xml`). Output is parsed with regexes to extract only relevant error messages — saving context window.
- **Stripe:** 3M+ test suite runs full CI after push. Autofixes auto-applied on failure for known patterns.
- **Webflow:** AI-generated test insertion into CI — tests are reviewed for coverage and quality before they gate deployments.

### Tier 2 — Invariant Gates

Business rule verification: idempotency, no double charges, ordering constraints. Catches failures that look correct locally but violate global guarantees. The checkout function works. The retry logic that calls it twice creates a duplicate charge. Invariant gates catch that.

Three questions to find your invariants: What must never happen twice? What must always be true after this operation completes? What breaks if operations run out of order?

→ [../tools/invariant-examples/](../tools/invariant-examples/) — Worked idempotent webhook example

### Tier 3 — Policy Gates

Security scanning, compliance checks, permission boundary enforcement. Catches violations of non-negotiable rules. For agents: sandboxing is non-negotiable. An agent with shell access on your host is a Remote Code Execution vulnerability by design.

**Who does this in production:**
- **Stripe:** Devbox isolation — pre-warmed EC2 instances with no internet, no production access, no real user data. Full agent permissions inside the box because the box is airtight. Internal security control framework blocks destructive MCP tool use.
- **Spotify:** Sandboxed containers with limited permissions, few binaries, virtually no access to surrounding systems. Three MCP tools only: verify, git (restricted subcommands), bash (allowlisted commands).

→ [agent-security/](agent-security/) — OWASP-mapped tooling for agent constraints

### Tier 4 — Behavioral Gates

Trace grading, behavioral baselining, drift detection, canary analysis. Catches failures no static check can see — an agent that suddenly reads 50 files instead of 5, a model whose quality score drifted 10 points over two weeks.

**LLM-as-judge:** Spotify runs a separate LLM that evaluates the agent's diff against the original task intent. It vetoes roughly 25% of sessions — primarily for scope creep, where the agent "fixed" things it wasn't asked to fix. This is a behavioral gate because no static analysis can detect scope creep. The judge model must be a different model instance (or different provider) than the one that generated the code, or you're grading your own homework.

**Who does this in production:**
- **Spotify:** LLM-as-judge runs after all deterministic verifiers pass. Agents course-correct ~50% of the time after a veto. As models improved, Spotify eventually removed the judge for some workflows — verification steps in prompts proved sufficient.
- **Stripe:** ~500 MCP tools in Toolshed, but curated subsets per task type. Rule files scoped to subdirectories and synced across Minions, Cursor, and Claude Code. Avoids unconditional global rules to preserve context window.
- **Spotify Ads:** Router agent classifies incoming messages to prevent unnecessary LLM calls, then dispatches to specialized parallel agents. One agent per skill/data source to prevent error amplification.

→ [agent-monitoring/](agent-monitoring/) — Step-by-step guide with code examples
→ [llm-as-judge-implementation.md](llm-as-judge-implementation.md) — Full implementation guide

### Tier 5 — Human Review

The least scalable gate. The most expensive. The only one that can answer "is this the right thing to build?"

Human review is not a rubber stamp after machine gates pass. It is the gate that catches what no machine can: wrong abstractions, misaligned intent, architectural decisions that make the system harder to change next quarter. Machine gates catch defects. Human review catches design mistakes.

**Who does this in production:**
- **Stripe:** 1,300+ PRs/week, all human-reviewed, zero human-written code. Human review is mandatory on every merge despite full agent autonomy during development.
- **Webflow:** Human code review on every PR, no exceptions. "You build it, you deploy it, you run it in prod" applies regardless of code origin.
- **Spotify:** Stop hook blocks PR creation if any verifier fails — the human reviewer never sees code that hasn't passed all machine gates first. This is the right sequence: machine gates clear the noise so human review time is spent on judgment, not bug-finding.
- **Webflow:** AI PR Linter (opt-in via GitHub label) invokes Claude Code with internal best practices to leave an informed review comment — augmenting human review, not replacing it.

---

## Agent Loop Gates

The tiers above describe *what* to verify. Agent loop gates describe *when and how* verification runs inside the agent's own execution cycle. These are the guardrails that prevent the agent from shipping code that hasn't passed verification — even if the agent thinks it's done.

**The principle: "The walls matter more than the model."** Deterministic, non-bypassable gates beat LLM self-policing every time. A model that promises to run tests before opening a PR will skip them 10% of the time. A stop hook that blocks PR creation if tests fail will skip them 0% of the time.

### Stop hooks

Configure your agent harness to block PR creation if verifiers fail. In Claude Code, this is a hook on the `pre-commit` or `post-tool-call` event. In Cursor, it's a rules file. The mechanism varies — the principle doesn't. The agent should be physically unable to open a PR when tests are red.

### CI retry with cap

Stripe's Minions architecture allows the agent to read CI failure logs and attempt a fix — but caps it at 2 rounds. If the second CI run fails, the task is kicked back to a human. Without the cap, agents will retry indefinitely, burning tokens and sometimes making the code worse with each attempt. Two rounds is enough to catch a typo or missing import. If the agent can't fix it in two tries, the problem requires human judgment.

### Sandbox isolation as a gate

Stripe's devboxes give each agent a sandboxed environment with no internet access and no production credentials. This isn't just a security measure — it's a verification gate. If the code only works because the agent reached out to a production API or read a real database, it will fail in the sandbox. The sandbox forces the agent to write code that works with the test infrastructure you've set up, not with production shortcuts.

### Visual regression gate

AI generates UI code confidently but cannot see what it renders. Unit tests verify behavior; visual regression gates verify appearance. Use Playwright screenshot assertions, Chromatic, or Percy to capture before/after screenshots of every UI change and flag visual diffs for human review. This catches layout breaks, styling regressions, and rendering bugs that no unit test or linter will detect. For any agent that touches frontend code, a visual regression gate belongs alongside your CI checks.

→ See [visual-regression-gate.md](visual-regression-gate.md) for setup guidance.

---

## For Agents: Start Here

**[agent-production-checklist.md](agent-production-checklist.md)** — Unified checklist synthesized from OpenAI, Anthropic, Google, NVIDIA, and Spotify. 8 sections, pass/fail, review cadence. Use before granting any agent production access.

---

## Contents

| Directory | What it is |
|-----------|-----------|
| [agent-production-checklist.md](agent-production-checklist.md) | Unified pass/fail checklist from all major providers |
| [observability/](observability/) | Three-layer observability guide: pipeline, delivery, and agent |
| [agent-monitoring/](agent-monitoring/) | Tracing, baselines, alerts, iteration budgets — with code |
| [agent-security/](agent-security/) | OWASP Top 10 mapped tooling: sandboxing, permissions, supply chain |
| [multi-pass-review/](multi-pass-review/) | Installable multi-perspective AI code review (`code-reviewers`) |
| [llm-as-judge-implementation.md](llm-as-judge-implementation.md) | Full LLM-as-judge setup guide with pseudocode |
| [stop-hooks-implementation.md](stop-hooks-implementation.md) | Block bad PRs before they open — Claude Code + GitHub Actions |
| [visual-regression-gate.md](visual-regression-gate.md) | Visual diffing setup for AI-generated UI code |
| [by-language/](by-language/) | Gate tooling for JS/TS, Python, Go, JVM, Rust, Ruby, PHP |

---

## Key Research

- [SmartBear/Cisco](https://static0.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf) — 2,500 reviews, 3.2M lines. 70-90% defect discovery at 200-400 lines. Collapses after 400.
- [CodeX-Verify (arXiv 2511.16708)](https://arxiv.org/abs/2511.16708) — Multi-perspective review improves accuracy from 32.8% to 72.4%
- [CodeRabbit (470 PRs)](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) — AI-authored code carries 1.7x more issues; XSS at 2.74x human rate
- [NYU Tandon (2021)](https://cyber.nyu.edu/2021/10/15/ccs-researchers-find-github-copilot-generates-vulnerable-code-40-of-the-time/) — ~40% of Copilot outputs contain exploitable vulnerabilities
- [GitClear (2025)](https://www.gitclear.com/ai_assistant_code_quality_2025_research) — AI code duplication at 8x the rate of human code; refactoring collapsed
- [Perry et al., Stanford (2023)](https://arxiv.org/abs/2211.03622) — Developers with AI rate code as more secure when it is measurably less so
- [OpenAI: Monitoring coding agents for misalignment](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/) — Tens of millions of interactions, ~1,000 moderate alerts, instrumental convergence
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — 100+ experts, 10 risk categories
