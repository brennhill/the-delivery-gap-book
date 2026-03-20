---
name: review
description: Three-pass code review (correctness → performance → security) that runs in series so later passes skip issues already flagged
disable-model-invocation: true
user-invocable: true
allowed-tools: Bash, Read, Grep
---

# Multi-Pass Code Review

Run three review passes in series against the current diff. Each pass sees the findings from prior passes and must not re-flag anything already identified.

## Get the diff

Run `git diff` to get unstaged changes. If empty, run `git diff --cached` for staged changes. If both are empty, run `git diff HEAD~1` to review the last commit. Tell the user which diff you are reviewing.

If the user passed an argument (a file path, PR number, or branch name), use that to scope the diff instead.

## Pass 1: Correctness & Logic

You are a senior engineer reviewing this diff for correctness and logic errors.

Focus primarily on:
- Does this code do what it claims to do?
- Off-by-one errors, boundary conditions, edge cases
- Null/undefined handling, empty collections, division by zero
- Missing early returns and guard clauses for unexpected inputs
- Incomplete error handling on I/O, network calls, and parsing
- Thread safety, race conditions, deadlocks
- Broken invariants (e.g., idempotency violations, double-writes)
- Wrong assumptions about data shapes or upstream behavior

Prioritize correctness and logic issues, but flag anything else you notice that could cause problems.

For each issue found, provide:
- File and line
- What the bug is
- Why it matters
- Suggested fix

If you find no issues, say "No correctness issues found." Do not invent problems.

Print findings under a `## Correctness & Logic` heading before continuing.

## Pass 2: Performance & Maintainability

You are a staff engineer reviewing the same diff for performance and maintainability.

**Do not re-flag anything already identified in Pass 1.**

Focus primarily on:
- N+1 queries, unbounded loops over external data
- Missing pagination on database queries or API calls
- Resource leaks (unclosed connections, file handles, streams)
- Algorithmic inefficiency (O(n^2) where O(n) is possible)
- Unnecessary complexity, dead code, unreachable branches
- Code duplication that will cause maintenance drift
- Readability issues that will cause review burden on future changes

For each issue found, provide:
- File and line
- What the problem is
- Expected impact (performance degradation, maintenance cost, etc.)
- Suggested fix

If you find no issues, say "No performance or maintainability issues found." Do not invent problems.

Print findings under a `## Performance & Maintainability` heading before continuing.

## Pass 3: Security & Scope

You are a security engineer reviewing the same diff for vulnerabilities and scope violations.

**Do not re-flag anything already identified in Pass 1 or Pass 2.**

Focus primarily on:
- SQL injection, XSS, command injection, path traversal
- Hardcoded credentials, API keys, secrets
- Insufficient input validation at system boundaries
- Authentication/authorization gaps
- Data exposure (PII in logs, sensitive data in error messages)
- Dependency vulnerabilities (known-bad versions)
- Scope violations (code touching resources it should not)
- Permission escalation patterns

For each issue found, provide:
- File and line
- What the vulnerability is
- Severity (Critical / High / Medium / Low)
- Suggested fix

If you find no issues, say "No security issues found." Do not invent problems.

Print findings under a `## Security & Scope` heading.

## Summary

After all three passes, print a `## Summary` with:
- Total issues found per pass
- Critical issues (if any) that should block merge
- One-line verdict: **PASS** (no critical issues), **REVIEW** (issues found but none critical), or **BLOCK** (critical issues that must be fixed)
