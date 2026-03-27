# General Spec Improvement Prompts

These prompts apply to any spec format. They target the four quality dimensions: ambiguity, testability, consistency, and completeness.

---

## Ambiguity

### Common gaps
- Adjectives without numbers ("fast", "scalable", "secure")
- Hedge words that defer decisions ("as needed", "when possible", "if applicable")
- Subjective terms with no shared definition ("user-friendly", "clean", "robust")

### Improvement questions
- For every adjective in your spec, can you replace it with a number?
- If two engineers read this spec independently, would they build the same thing?
- Would an AI agent interpret "handle errors appropriately" the same way you would?

### Before/After
- **Weak:** The system should be fast and handle errors appropriately.
- **Strong:** Response time MUST be under 200ms at p95. All errors return `{"error": "CODE", "message": "detail"}` with the corresponding HTTP status code.

---

## Testability

### Common gaps
- Requirements that can't be verified with a pass/fail test
- Goals without corresponding acceptance criteria
- Success defined as a feeling ("users should find it intuitive") rather than an observable behavior

### Improvement questions
- For each MUST/SHALL statement, can you write a single test that either passes or fails?
- If you handed this spec to QA with no other context, could they write a test plan?
- Is every requirement independently verifiable, or do some depend on subjective judgment?

### Before/After
- **Weak:** The system MUST authenticate all requests properly.
- **Strong:** The system MUST authenticate all requests. Given an unauthenticated request, When it hits any endpoint, Then return 401 with body `{"error": "unauthenticated"}`.

---

## Consistency

### Common gaps
- Scope exclusions that contradict acceptance criteria
- Requirements that conflict with constraints
- Terminology drift (same concept called different names in different sections)

### Improvement questions
- Read your "out of scope" section. Now read your acceptance criteria. Do any ACs reference things you excluded?
- Does every entity name appear exactly the same way everywhere? (e.g., "User" vs "Account" vs "customer")
- Do your constraints and requirements agree? If you say "no external dependencies" but an AC requires calling a third-party API, which wins?

### Before/After
- **Weak:** Out of scope: payment processing. AC: Given an order, When checkout completes, Then process payment and return confirmation.
- **Strong:** Out of scope: payment processing. AC: Given an order, When checkout completes, Then create a pending order record and emit an `order.created` event (payment handled by separate service).

---

## Completeness

### Common gaps
- Missing sections that the format expects
- Sections present but with placeholder content ("TBD", "N/A", "TODO")
- Template headers copied but not filled in

### Improvement questions
- Does every section header have substantive content beneath it (not just placeholders)?
- Are there sections your format expects that you haven't included? (Run `upfront quality` to check.)
- If you removed every section header, would the remaining content still make sense as a spec?

### Before/After
- **Weak:** ## Edge Cases\nTBD
- **Strong:** ## Edge Cases\n- What happens when the user submits an empty form?\n- What happens when the session expires mid-checkout?\n- What happens when two users edit the same record concurrently?
