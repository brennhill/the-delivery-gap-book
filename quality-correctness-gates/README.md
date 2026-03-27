# Quality-Correctness Gates — The Quality Gate Tiers

The Verification Triangle tells you what to measure. Gates are what make the eval quality vertex strong. Without gates, the weekly review is reading gauges on a pipeline with no valves.

Five tiers of verification, each catching a failure class the tier below cannot see. The tiers are cumulative — you cannot skip to Tier 3 without Tier 0.

---

## The Five Tiers

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

### Tier 1 — Contract Gates

API contract checks: does the interface behave as documented? Schema validation on all AI-generated outputs. Catches silent breakage between services — the failure that shows up three weeks later when nobody remembers what changed.

### Tier 2 — Invariant Gates

Business rule verification: idempotency, no double charges, ordering constraints. Catches failures that look correct locally but violate global guarantees. The checkout function works. The retry logic that calls it twice creates a duplicate charge. Invariant gates catch that.

Three questions to find your invariants: What must never happen twice? What must always be true after this operation completes? What breaks if operations run out of order?

→ [../tools/invariant-examples/](../tools/invariant-examples/) — Worked idempotent webhook example

### Tier 3 — Policy Gates

Security scanning, compliance checks, permission boundary enforcement. Catches violations of non-negotiable rules. For agents: sandboxing is non-negotiable. An agent with shell access on your host is a Remote Code Execution vulnerability by design.

→ [agent-security/](agent-security/) — OWASP-mapped tooling for agent constraints

### Tier 4 — Behavioral Gates

Trace grading, behavioral baselining, drift detection, canary analysis. Catches failures no static check can see — an agent that suddenly reads 50 files instead of 5, a model whose quality score drifted 10 points over two weeks.

→ [agent-monitoring/](agent-monitoring/) — Step-by-step guide with code examples

---

## For Agents: Start Here

**[agent-production-checklist.md](agent-production-checklist.md)** — Unified checklist synthesized from OpenAI, Anthropic, Google, NVIDIA, and Spotify. 8 sections, pass/fail, review cadence. Use before granting any agent production access.

---

## Contents

| Directory | What it is |
|-----------|-----------|
| [agent-production-checklist.md](agent-production-checklist.md) | Unified pass/fail checklist from all major providers |
| [observability/](observability/) | Three-layer observability guide: pipeline, delivery, and agent |
| [agent-monitoring/](agent-monitoring/) | Tracing, baselines, alerts, LLM-as-judge — with code |
| [agent-security/](agent-security/) | OWASP Top 10 mapped tooling: sandboxing, permissions, supply chain |
| [multi-pass-review/](multi-pass-review/) | Installable multi-perspective AI code review (`code-reviewers`) |
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
