# Spec Best Practices

A spec is the document that makes verification possible. Without it, every gate downstream is checking against nothing.

## What a spec must contain

1. **User-facing change** — what the user will see or experience differently
2. **Non-negotiable constraints** — what must never break (e.g., "no double charges", "response under 200ms")
3. **Out of scope** — what this change explicitly does not do
4. **Architectural boundaries** — which services, databases, and APIs are touched
5. **Acceptance criteria** — how you know it works, stated as testable conditions

## What a spec is not

- A Jira ticket title
- A one-line prompt
- A "we'll figure it out as we go" placeholder
- A copy of the PR description written after the code

## When to write a spec

Before AI-assisted implementation begins on any change above Risk Tier 1. The spec exists so the AI has constraints. Without constraints, the AI fills every gap with confident fiction.

## Enforcement

PRs without a linked spec for Risk Tier 2+ changes go back before review starts. This is a process decision, not a technical one:

- Add a "Spec Link" field to your PR template (required, not optional)
- CI can check: does the field contain a valid URL or ticket ID?
- Placeholders like "TBD", "pending", or empty fields count as no-spec

## How to know if your specs are working

Run `spec-coverage.py` to measure coverage. Then run `rework-by-spec.py` to compare rework rates. If spec'd changes have the same rework rate as unspec'd changes, your specs are performative — they exist but don't constrain anything useful.

## The one-page spec template

See [templates/specs/01-one-page-spec-template.md](../../templates/specs/01-one-page-spec-template.md) for a ready-to-use template.

## Research basis

- CodeScout (arXiv:2603.05744): converting underspecified problem statements into detailed specifications improved resolution rates by 20% on SWE-bench Verified
- Montgomery et al.: ambiguity and incompleteness remain central requirements-quality concerns with downstream delivery effects
- Albayrak et al.: incomplete requirements force engineers to fill gaps with assumptions, pushing risk downstream
