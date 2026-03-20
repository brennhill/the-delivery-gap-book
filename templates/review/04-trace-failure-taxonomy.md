# Trace Failure Taxonomy

Use one primary class per incident, with optional secondary class.

## Primary classes
1. Correctness: wrong behavior/output.
2. Contract: interface/schema mismatch.
3. Policy: security/compliance breach.
4. Process: bad sequence/tool path/retry behavior.
5. Quality drift: still functional, materially worse output quality.

## Required fields
- Incident ID:
- Trace ID:
- First bad span:
- Primary class:
- Secondary class:
- Side effects occurred: yes/no
- Containment action:
- Prevention action:
- Owner:

## Quick triage flow
1. Find first bad span.
2. Classify failure.
3. Confirm side effects.
4. Contain now.
5. Add one deterministic prevention check.
