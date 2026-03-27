# Quick-Start Guides

These guides get your team from zero to Tier 0 verification gates in one sitting.

## Who these are for

Teams adopting AI-assisted development who want a minimum safety net in CI before code reaches human reviewers. Each guide picks one tool per job, explains what it catches and what it misses, and tells you exactly what your CI pipeline should enforce.

## What they cover

**Tier 0 only** — static analysis, formatting, secret detection, and PR size limits. This is the floor, not the ceiling. Tier 0 catches the cheap stuff so reviewers can focus on the hard stuff.

Available guides:

- [TypeScript / JavaScript](typescript.md)
- [Python](python.md)
- [Go](go.md)
- [JVM (Java / Kotlin)](jvm.md)

## What they do NOT cover

Tiers 1-3 (test coverage, property testing, contract testing, architecture enforcement, etc.). For those, see the [by-language reference pages](../quality-correctness-gates/by-language/).

## Guided setup

For a guided setup, use the AI-assisted setup via `CLAUDE.md` in the repo root. It will walk you through tool selection, configuration, and CI integration interactively.
