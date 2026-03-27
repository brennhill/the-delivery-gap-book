# SWE Spec Improvement Prompts

Section-by-section prompts for the Context-Anchor Spec (delivery-gap format). Use alongside `01-one-page-spec-template.md`.

---

## Context: "For Whom" and "Why Now"

### Common gaps
- Missing the user persona — who specifically benefits?
- No urgency signal — why this sprint, not next quarter?
- Feature described but problem not stated

### Improvement questions
- Who is the specific user or role affected by this change?
- What happens if we don't build this? What breaks, what's blocked?
- Can you state the problem in one sentence without mentioning the solution?

### Before/After
- **Weak:** Add authentication to the API.
- **Strong:** External partners are blocked from integrating because our API has no auth. Without this, the Q2 partner launch slips.

---

## Model Anchors: "Where the AI should look"

### Common gaps
- No file paths — AI guesses where to put code
- References to "the codebase" without specific modules
- Missing API specs or schema references

### Improvement questions
- Which specific files should the AI read before writing code?
- Is there an existing pattern the AI should follow? Point to it with `src/path/file.ts`.
- Are there API specs (OpenAPI, GraphQL schema) the AI should conform to?

### Before/After
- **Weak:** Follow existing patterns.
- **Strong:** Follow the pattern in `src/auth/handler.ts`. Conform to `openapi/v2.yaml` for endpoint shapes. Use the `BaseService` class from `src/services/base.ts`.

---

## Scope Boundaries

### Common gaps
- "In scope" is vague or just restates the feature name
- No explicit non-goals — AI invents adjacent work
- Boundaries don't mention adjacent features that should NOT be touched

### Improvement questions
- What will the AI be tempted to build that you don't want?
- Are there adjacent features that look related but should not change?
- If the AI "finishes early," what should it NOT add?

### Before/After
- **Weak:** In scope: authentication. Out of scope: everything else.
- **Strong:** In scope: JWT-based auth for REST endpoints. Non-goals: OAuth/SSO integration, admin user management, rate limiting (handled by API gateway).

---

## Constraints and Non-negotiables

### Common gaps
- Constraints without numbers ("must be fast", "must be secure")
- Missing compliance or policy requirements
- No SLA or reliability targets

### Improvement questions
- For each constraint, what is the number? Latency in ms? Uptime percentage? Max payload size?
- Are there compliance requirements (SOC2, HIPAA, GDPR) that constrain the implementation?
- What is the maximum acceptable error rate? Downtime window?

### Before/After
- **Weak:** Must be secure and performant.
- **Strong:** All endpoints MUST require OAuth2 bearer tokens. Response time MUST be under 200ms at p95. Error rate MUST stay below 0.1% over any 5-minute window.

---

## Key Entities

### Common gaps
- Entities mentioned in ACs but never defined
- No field types or relationships specified
- Implicit entities (like "session" or "token") that the AI needs to know about

### Improvement questions
- List every noun that appears in your acceptance criteria. Is each one defined?
- For each entity, what fields does it have? What are the types?
- What are the relationships between entities? (User has many Tokens? Order belongs to User?)

### Before/After
- **Weak:** Users can create orders.
- **Strong:** **User**: `{id: UUID, email: string, role: enum(admin|member)}`. **Order**: `{id: UUID, user_id: FK(User), status: enum(DRAFT|PENDING|COMPLETE), total_cents: int}`. A User has many Orders.

---

## Style and Architecture Rules

### Common gaps
- No module boundaries — AI sprawls across packages
- No error/logging conventions — AI invents per-function patterns
- Missing naming conventions

### Improvement questions
- Which modules/packages should this code live in? Which should it NOT touch?
- What is the error handling convention? (Return errors? Throw? Error type?)
- What logging pattern should new code follow? (Structured? Which logger? What level?)

### Before/After
- **Weak:** Follow best practices.
- **Strong:** All code lives in `src/auth/`. Do not modify `src/billing/` or `src/admin/`. Errors use `AppError(code, message)` — never throw raw exceptions. Log at INFO for success, WARN for retries, ERROR for failures using the structured logger from `src/observability/logger.ts`.

---

## Acceptance Criteria

### Common gaps
- Criteria that describe behavior but not observable outcomes
- Missing response codes, body shapes, or state changes
- No negative cases (what happens when it fails?)

### Improvement questions
- For each criterion, what HTTP status code is returned? What is the response body shape?
- What happens when the input is invalid? What error does the user see?
- Can each criterion be verified with a single automated test?
- Have you covered both the happy path and at least one failure path?

### Before/After
- **Weak:** Users can log in successfully.
- **Strong:** Contract check: POST /login with valid credentials returns 200 with `{token: string, expires_at: ISO8601}`. Invariant check: POST /login with invalid credentials returns 401 with `{error: "invalid_credentials"}`. Policy check: POST /login is rate-limited to 10 attempts per minute per IP.

---

## Error Contract

### Common gaps
- No standard error shape — each endpoint invents its own
- Missing error codes for known failure modes
- No guidance on what gets logged vs. what gets returned to the client

### Improvement questions
- What is the standard error response shape? (e.g., `{"error": "code", "message": "detail"}`)
- For each endpoint, what are the possible error codes and when do they fire?
- What information is safe to return to the client vs. what should only be logged?

### Before/After
- **Weak:** Handle errors gracefully.
- **Strong:** All errors return `{"error": "ERROR_CODE", "message": "human-readable detail", "request_id": "uuid"}`. Error codes: `unauthenticated` (401), `forbidden` (403), `not_found` (404), `rate_limited` (429), `internal` (500). Internal error details are logged but never returned to the client.

---

## Edge Cases

### Common gaps
- Only happy-path behavior specified
- No concurrent/race condition scenarios
- No boundary value cases (empty, null, max size)

### Improvement questions
- What happens when [entity] is empty? null? at max size?
- What happens when [entity] is deleted while in use by another process?
- What happens when two users perform the same action simultaneously?
- What happens when an external dependency (database, API, queue) is down?
- What happens at midnight, at year boundaries, during daylight saving transitions?

### Before/After
- **Weak:** The system handles edge cases.
- **Strong:** Edge cases:\n- Empty cart checkout: return 400 with `{error: "empty_cart"}`\n- Concurrent edit: last-write-wins with optimistic locking (409 on version mismatch)\n- Payment gateway timeout: retry once after 3s, then fail with `{error: "payment_timeout"}`

---

## Rollback Plan

### Common gaps
- No trigger signal — when do we know it's broken?
- Rollback method unclear (toggle? revert? blue-green?)
- No owner assigned for the rollback decision

### Improvement questions
- What metric or alert tells you this change is broken in production?
- Can you roll back with a feature toggle, or does it require a code revert?
- Who has authority to trigger the rollback? (On-call? DRI? Anyone?)

### Before/After
- **Weak:** Rollback if something goes wrong.
- **Strong:** Trigger: error rate > 5% on /login endpoint for 5 minutes (PagerDuty alert). Method: feature toggle `auth_v2_enabled` set to false (instant, no deploy). Owner: on-call engineer has authority to toggle without approval.
