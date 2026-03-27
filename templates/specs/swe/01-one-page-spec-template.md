# Delivery Spec Template

> See [the spec process guide](../README.md) for how and when to fill this out.
> Best filled out interactively using the `/feature` command, which walks you through each section with pushback and codebase research.

Four sections, each building on the last. Do not skip ahead.

---

## Intent

*WHY are we doing this? Answer before anything else. The `/feature` command will challenge vague answers.*

### 1. What problem does this solve?
*Not what does it build — what problem goes away?*

### 2. How will we know it worked?
*An existing metric that will move, not one invented for the project.*

### 3. What is out of scope?
*Explicit boundaries the AI must not cross.*

### 4. What must NOT happen?
*Constraints and negation — the genie's missing instructions.*

### 5. Pre-mortem findings
*30 minutes: why could this fail?*

---

## Behavioral Spec

*WHAT does the user experience? Work through this interactively — stories first, then mechanism, then states, then errors.*

### User Stories
*Walk through the current experience, then the desired experience. What does the user do, see, get back?*

### Mechanism
*Why will this approach solve the problem? What assumptions are we making?*

### States and Transitions
*What are all the states this feature can be in? What moves it between them? What does the user see in each?*

### Error Cases
*What happens when dependencies fail? Concurrent requests? Unexpected user behavior? Edge cases?*

---

## Design Approach

*HOW will we approach this conceptually? The `/feature` command researches the codebase and presents options.*

### Conceptual approach
*The chosen approach and why. Alternatives considered.*

### Codebase context
*How similar features work in this codebase. Relevant patterns found.*

---

## Implementation Design

*HOW specifically — where does the code go? The `/feature` command researches placement and challenges the codebase.*

### Architecture
*Where code lives, data models (conceptual), interfaces, integration points.*

### Structural issues flagged
*Any codebase slop, inconsistent patterns, or cleanup needed as prerequisites.*

### Constraints and Non-negotiables
*Machine-readable version of intent Q4. Use numbers: latency in ms, error rate thresholds, specific invariants.*
- Security:
- Reliability/SLA:
- Compliance/policy:

### Known AI Blind Spots
*LLMs fail systematically, not randomly. Check each item or mark N/A.*
- [ ] **Edge cases**: boundary values, empty/null/max-size inputs, off-by-one
- [ ] **Concurrency**: race conditions, concurrent writes, optimistic locking needs
- [ ] **Error handling**: what happens when each dependency is down or slow?
- [ ] **Security**: auth on every endpoint, input validation, no secrets in logs/responses
- [ ] **Non-prompted concerns**: rate limiting, pagination, logging, audit trails, idempotency
- [ ] **Hallucination risk**: are all referenced packages, APIs, and imports real? Pin versions.

### Rollback Plan
- Trigger signal:
- Method: (Toggle/Revert/Fallback)
- Owner:

### Ownership
- DRI:
- Reviewers:
- Decision date:
