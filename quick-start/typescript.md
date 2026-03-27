# Quick Start: TypeScript / JavaScript

> This guide covers Tier 0 (static analysis) only. It is a starting point, not complete verification. See the [by-language reference](../quality-correctness-gates/by-language/javascript-typescript.md) for higher tiers.

## What you need running in CI

### 1. Linter + Formatter: Biome

Biome replaces ESLint + Prettier with a single tool. It is faster, requires less configuration, and produces consistent output.

Your CI should run `biome check .` and fail if it exits non-zero.

**Alternative:** If your project already uses ESLint + Prettier and the config is stable, keep it. The goal is enforcement, not migration.

### 2. Type checking: tsc

Your CI should run `tsc --noEmit --strict` and fail on any type error. This catches type mismatches, missing properties, and incorrect function signatures without producing build artifacts.

If you are a JavaScript-only project, add a `tsconfig.json` with `allowJs: true` and `checkJs: true` to get type checking without converting files.

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

AI-generated TypeScript frequently introduces unused imports, `any` type assertions, subtle type mismatches, and occasionally hardcoded credentials or API keys. Large AI-generated PRs also tend to bundle unrelated changes.

- **Biome** catches formatting drift, unused variables, unreachable code, and import issues.
- **tsc --strict** catches type errors that pass linting but break at runtime.
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

See the [by-language reference](../quality-correctness-gates/by-language/javascript-typescript.md) for Tiers 1-3.

## Next steps

1. Read the [TypeScript / JavaScript by-language page](../quality-correctness-gates/by-language/javascript-typescript.md) for testing, property testing, and architecture enforcement options.
2. Use the AI-assisted setup via `CLAUDE.md` in the repo root for guided configuration of higher tiers.
