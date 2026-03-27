# Quick Start: Python

> This guide covers Tier 0 (static analysis) only. It is a starting point, not complete verification. See the [by-language reference](../quality-correctness-gates/by-language/python.md) for higher tiers.

## What you need running in CI

### 1. Linter + Formatter: Ruff

Ruff replaces Flake8, Black, isort, pyupgrade, and dozens of other tools with a single Rust-based binary. It is 10-100x faster and uses a single config file (`ruff.toml` or `pyproject.toml`).

Your CI should run `ruff check .` and `ruff format --check .` and fail if either exits non-zero.

**Alternative:** If your project uses Flake8 + Black + isort and the config is stable, keep it. But for new projects, Ruff is the clear default.

### 2. Type checking: mypy

Your CI should run `mypy --strict .` and fail on any type error. This catches incorrect argument types, missing return types, and None-safety issues.

**Alternative:** Pyright is faster and catches some errors mypy misses, particularly around type narrowing. Either is fine for Tier 0; pick one and enforce it.

### 3. Secret detection: TruffleHog

Your CI should run TruffleHog against the diff (not the full repo history on every PR). It scans for API keys, tokens, database credentials, and private keys using both pattern matching and entropy analysis.

Run `trufflehog git --since-commit=<base> --fail` and fail the pipeline on any finding.

### 4. PR size limits

Enforce diff size on every pull request:
- **Warn** at 400 changed lines
- **Soft block** at 500 lines (require justification comment to merge)
- **Hard block** at 1,000 lines (must be split)

Use your CI platform's API or a bot to count lines changed and post a status check.

## What each catches

AI-generated Python frequently introduces unused imports, incorrect type annotations, inconsistent formatting, and occasionally hardcoded credentials. Large AI-generated PRs also tend to bundle unrelated changes.

- **Ruff** catches style violations, unused imports, unreachable code, and common bug patterns (from hundreds of enabled rules).
- **mypy --strict** catches type errors that would surface as runtime TypeErrors or AttributeErrors.
- **TruffleHog** catches secrets that should never reach the repo.
- **PR size limits** force decomposition, making review tractable.

These checks are cheap, fast, and block the most common AI-generated defects before a human ever opens the PR.

## What this does NOT catch

Tier 0 catches formatting and obvious errors. It does not catch:

- Business logic bugs
- API contract drift between services
- Race conditions or concurrency issues
- Security vulnerabilities beyond leaked secrets
- Missing or inadequate test coverage

See the [by-language reference](../quality-correctness-gates/by-language/python.md) for Tiers 1-3.

## Next steps

1. Read the [Python by-language page](../quality-correctness-gates/by-language/python.md) for testing, property testing, and architecture enforcement options.
2. Use the AI-assisted setup via `CLAUDE.md` in the repo root for guided configuration of higher tiers.
