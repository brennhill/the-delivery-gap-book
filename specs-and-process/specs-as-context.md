# Specs as Context: What to Document, When, and Why

## What a Spec Is Not

A spec is not a build instruction. AI does not need a spec to write code — it needs context, constraints, and verification criteria. If you hand an agent a 20-page spec and say "build this," the agent will read the first page, skim the rest, and hallucinate the details. The spec did not help. The code is the implementation. The spec cannot compete with the code for describing what the code does.

**A spec is not a prevention mechanism.** Research shows that upfront specs do not improve code quality. They do not prevent defects. The code IS the spec for what the system does — no document can substitute for reading it.

## What a Spec Is

A spec documents everything the code cannot tell you.

The code tells you what the system does. It does not tell you:

- **Why** it does it that way (the business reasoning, the tradeoff that was made, the constraint that drove the decision)
- **Who** else is affected (upstream teams waiting on this API, downstream consumers who depend on this format, the compliance team who needs audit evidence)
- **What must not change** (business invariants that are implicit in the code but invisible to someone — or some agent — reading it for the first time)
- **What was considered and rejected** (the approach that looked obvious but would have broken the billing integration, the shortcut that would have violated the SLA)
- **What happens outside the code** (manual steps in a deployment, a Slack notification that has to go to legal, a data migration that runs once)

When an agent reads your codebase next month, it sees functions and types. It does not see that the retry logic in the payment handler exists because Stripe's webhook delivery has a known 3-second latency spike on Tuesdays, and the finance team will file an incident if a charge is duplicated. That context is either in a spec or it is in someone's head. Heads leave the company. Specs stay.

## The Three Purposes

### 1. Alignment

Before you build, the spec aligns the people involved on what problem is being solved and what "done" looks like. Not the implementation — the intent and constraints. This is the /feature workflow: five forcing-function questions, behavioral spec, design conversation, implementation design. The spec captures the thinking, not the code plan.

The alignment purpose is served by writing the spec conversationally, as you go, not by writing a document and throwing it over a wall. The spec grows as understanding grows. It is not a prerequisite for starting — it is a byproduct of starting well.

### 2. Auditing

After you build, the spec is the audit trail. When someone asks "why does this work this way?", the answer is in the spec's thinking records — what was decided, what was rejected, what data was consulted, what risks were accepted. This is more valuable than git blame, which tells you who changed a line but not why the line exists.

For regulated industries, the audit trail is not optional. For everyone else, it is the difference between institutional memory and institutional amnesia.

### 3. Handover

When someone else — human or agent — picks up this work, the spec tells them what the code cannot. The business invariants. The constraints that are not enforced by tests. The teams that need to be notified. The decisions that were made and the reasoning behind them.

An agent inheriting a codebase without specs will make confident, plausible decisions that violate constraints it cannot see. It will refactor the payment handler to remove the "unnecessary" retry logic. It will change the API response format without knowing that the mobile team parses it with a regex. It will delete the "dead code" that runs once a quarter for the compliance audit.

---

## What Goes in a Spec

### Always document (the code cannot tell you)

| Category | Examples |
|----------|---------|
| **Business WHY** | Why this feature exists. What problem it solves. What metric it moves. |
| **Invariants** | "A charge must never be duplicated." "The audit log must never be truncated." "The user's email must be verified before they can access billing." These are implicit in the code but invisible to a reader who does not know the domain. |
| **Cross-team dependencies** | Other teams consuming this API. Upstream services that feed this data. SLAs or contracts with external partners. |
| **Constraints not enforced by code** | Compliance requirements. Performance SLAs. Data residency rules. Manual steps in the deployment process. |
| **Decisions and reasoning** | What was considered. What was rejected and why. What tradeoffs were accepted. |
| **Out of scope** | What was explicitly decided not to build. Without this, the next person (or agent) will build it, thinking it was simply forgotten. |
| **Rollback plan** | How to undo this if it goes wrong. Who owns the decision. What signal triggers it. |

### Never document (the code already tells you)

- Implementation details (function signatures, data structures, algorithms)
- File locations and module structure
- API schemas (these should be generated from code, not maintained separately)
- Step-by-step build instructions (the code and tests ARE the build instructions)

If you find yourself copying code into a spec, you are documenting the wrong thing.

---

## When to Write: Spec as You Go

Do not write the spec before building. Do not write the spec after building. Write the spec while building.

### Before you start (5 minutes)

Write the intent block: what problem, what metric, what is out of scope, what must not happen. This is not a detailed spec. It is a constraint envelope — the boundaries within which iteration happens. If you cannot write these four things in 5 minutes, you do not understand the problem well enough to start.

### During iteration (continuous)

As you make decisions, document them in the spec. Not every decision — the ones that would be invisible to a future reader of the code:

- "We chose polling over webhooks because the vendor's webhook delivery is unreliable during peak hours."
- "The retry limit is 3 because finance considers any charge duplication above 0.01% an incident."
- "This endpoint does not paginate because the maximum result set is bounded by the number of active projects per org (< 100)."

This takes seconds per decision. It is not a ceremony. It is capturing the WHY while the WHY is still in your working memory.

### After each phase (10 minutes)

When a chunk of work is complete — a PR is merged, a milestone is reached — update the spec's thinking record. What was decided. What was rejected. What surprised you. What risks you accepted. This is the audit trail.

### On handover

When someone else will touch this code — another engineer, an agent, a future you who has forgotten the context — review the spec and ask: "If I read only this document and the code, would I know enough to make good decisions?" If the answer is no, the spec is missing something.

---

## Context Engineering and Specs

Context engineering is the practice of giving AI the right information at the right time. Specs are one layer of context — the layer that carries business intent, constraints, and reasoning that the code alone cannot convey.

The context stack for an agent working on your codebase:

| Layer | What it provides | Where it lives |
|-------|-----------------|----------------|
| **Code** | What the system does, how it is structured | Source files |
| **Tests** | What the system must do, edge cases, invariants | Test files |
| **CLAUDE.md / rules** | Conventions, boundaries, build commands, what not to do | Context files |
| **Specs** | Business WHY, cross-team dependencies, invariants not in code, decision history | Spec files |
| **Documentation** | API contracts, architecture diagrams, onboarding guides | Docs |

Each layer answers questions the others cannot. Code without specs produces agents that are technically correct and business-wrong. Specs without code produce agents that hallucinate implementations. The layers are complementary.

**Specs reduce agent token waste.** An agent without a spec reads dozens of files trying to infer why something works the way it does. An agent with a spec reads the spec, gets the constraints, and writes code that respects them on the first pass. Fewer iterations, fewer rework cycles, lower cost per accepted change.

**Specs make LLM-as-judge effective.** The judge evaluates whether the agent's output matches the original intent. Without a spec, the judge is comparing the diff against a vague prompt. With a spec, the judge has explicit success criteria, invariants, and out-of-scope boundaries to check against. The spec is what makes intent alignment verifiable.

---

## The Spec Lifecycle

```
Problem identified
    → Write intent block (5 min)
    → Iterate: build, learn, document decisions as you go
    → Phase complete: update thinking record (10 min)
    → Ship: spec is the audit trail
    → Handover: spec is the context for the next person or agent
    → Maintenance: update spec when invariants or constraints change
    → Retirement: spec stays as historical record even after code is removed
```

The spec is a living document during development and a historical record after. It is never a gatekeeping artifact that must be "approved" before work begins. If your spec process requires approval before iteration, you have reinvented waterfall with a different name.

---

## What This Means for the Feature Workflow

The `/feature` command in this toolkit walks through intent, behavioral spec, design, and implementation design. Each phase produces a thinking record — decisions, reasoning, rejected alternatives, risks accepted.

That output IS the spec. You did not write a spec and then build. You thought through the problem, captured the thinking, and now have a document that serves alignment, auditing, and handover. The spec was a byproduct of good process, not a prerequisite for permission to start.

If you skip `/feature` and go straight to code, you can still spec as you go — just capture the decisions as you make them. The format matters less than the discipline: every time you make a decision that would be invisible in the code, write it down.
