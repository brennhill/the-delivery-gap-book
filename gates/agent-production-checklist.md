# Agent Production Readiness Checklist

A unified checklist synthesized from OpenAI, Anthropic, Google, NVIDIA, and Spotify's published production practices. Use this before granting any agent production access.

---

## 1. Scope & Permissions

- [ ] Agent's scope is documented: what it can do, what it cannot do
- [ ] Scope is **enforced** by tool allowlist, not just described in a system prompt
- [ ] Permissions are minimum-necessary and documented per-agent
- [ ] Permissions were granted by a named owner with a date
- [ ] Short-lived, scoped tokens used (not long-lived credentials or developer keys)
- [ ] Agent cannot escalate its own permissions
- [ ] Out-of-scope requests are tested and confirmed to be rejected

> **Why:** OpenAI found their own agents extracting encrypted credentials and bypassing content scanning — not through malice, but because agents treat security controls as obstacles to solve. Scope enforcement must be infrastructure, not instructions.

---

## 2. Sandbox & Isolation

- [ ] Agent runs in an isolated environment (Docker at minimum)
- [ ] No host filesystem mount
- [ ] No environment variable passthrough
- [ ] Outbound network restricted to allowlisted endpoints only
- [ ] Default-deny posture: agent starts with nothing and earns access

**Choose your isolation level:**

| Risk Tier | Minimum Sandbox |
|-----------|----------------|
| Tier 1 (docs, tests, internal tools) | Docker (rootless) |
| Tier 2 (customer-facing, APIs) | gVisor or NVIDIA OpenShell |
| Tier 3 (billing, auth, PII) | Firecracker microVM, or no agent access |

> **Why:** Google ADK, NVIDIA OpenShell, and OpenAI Codex all implement default-deny. An agent with shell access on your host is a Remote Code Execution vulnerability by design.

---

## 3. Input Filtering & Guardrails

- [ ] User inputs are validated before reaching the agent
- [ ] Prompt injection defenses are in place (input sanitization, instruction hierarchy)
- [ ] Agent cannot process untrusted external content without sandboxing
- [ ] Token/context limits are enforced to prevent context stuffing attacks
- [ ] System prompts are protected from extraction or override

> **Why:** OpenAI and Anthropic both recommend input filtering as the first line of defense. OWASP Agentic #7 (Vulnerable Integration Points) covers this.

---

## 4. Exit Conditions & Limits

- [ ] Hard cap on iterations (e.g., 10 max)
- [ ] Timeout enforced (e.g., 5 minutes)
- [ ] Token budget enforced (e.g., 100K tokens)
- [ ] When limits are hit, agent returns partial result with status — not silent continuation
- [ ] Retry behavior is bounded (no infinite retry loops)

> **Why:** Stripe limits agents to 2 CI runs per task. Without iteration limits, a looping agent burns tokens and can produce cascading side effects.

---

## 5. Human Override

- [ ] Kill switch exists and has been tested
- [ ] Agent can be stopped within 30 seconds
- [ ] In-progress work is rolled back or left in a documented safe state on interruption
- [ ] Kill switch is tested monthly (not just documented)

> **Why:** Meta's alignment director could not stop her own agent — she had to physically pull the network cable. Test the stop mechanism before you need it.

---

## 6. Audit Trail

- [ ] Every tool call logged with timestamps and trace IDs
- [ ] Every decision point logged (not just final output)
- [ ] Authorization context recorded (who approved, what permissions)
- [ ] Logs retained per your organization's policy
- [ ] Logs can be queried after the fact to reconstruct what happened and why

> **Why:** OWASP #3 (Insufficient Decision Transparency). If you cannot reconstruct what the agent did, you cannot investigate incidents, satisfy auditors, or improve the system.

---

## 7. Monitoring & Behavioral Baseline

- [ ] Structured traces captured for every session (tool calls, file access, token usage, duration)
- [ ] Behavioral baseline established from first 2 weeks of production data
- [ ] Anomaly alerts configured:
  - [ ] File access count > 3x p95
  - [ ] Token usage > 5x median
  - [ ] Session duration > 5x median
  - [ ] Any tool call not seen in baseline period
  - [ ] Any outbound network call not on allowlist
- [ ] LLM-as-judge sampling configured (5-10% of sessions reviewed by a separate model)
- [ ] Alert-to-action ratio tracked (target: at least 1 in 3 alerts leads to investigation)

> **Why:** OpenAI's monitoring caught ~1,000 moderate-severity issues across millions of interactions. Spotify's LLM-as-judge vetoes ~25% of sessions. These catches are invisible without monitoring infrastructure.

---

## 8. Blast Radius Assessment

- [ ] Worst-case scenario documented: "If this agent does the worst thing it's technically capable of, what happens?"
- [ ] Worst case accepted in writing by engineering lead
- [ ] Blast radius bounded by sandbox and permission constraints
- [ ] For destructive operations: explicit approval token required before execution
- [ ] Rollback path documented and tested

> **Why:** Every production deletion in the incident record happened because nobody assessed worst-case behavior before granting access.

---

## Review Cadence

- [ ] **Before launch:** Complete this checklist. Every item pass/fail with a named reviewer and date.
- [ ] **Monthly:** Test kill switch. Review alert-to-action ratio. Update baseline if agent configuration changed.
- [ ] **Quarterly:** Full permission audit. Rerun checklist. Update threat profile against OWASP Top 10 for Agentic Applications.

---

## Sources

This checklist synthesizes production practices from:

- [OpenAI: How we monitor internal coding agents for misalignment](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/)
- [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- [Anthropic: Building Effective AI Agents](https://resources.anthropic.com/building-effective-ai-agents)
- [Anthropic: Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Anthropic: Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Google ADK: Safety and Security for AI Agents](https://google.github.io/adk-docs/safety/)
- [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell)
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- Stripe Minions architecture (Stripe Dev Blog, 2026)
- Spotify Honk system (Spotify Engineering Blog, 2025)
