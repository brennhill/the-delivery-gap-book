# Quick Start: Go

> This guide covers Tier 0 (static analysis) only. It is a starting point, not complete verification. See the [by-language reference](../quality-correctness-gates/by-language/go.md) for higher tiers.

## What you need running in CI

### 1. Linter: golangci-lint

golangci-lint aggregates 50+ linters behind a single binary and config file (`.golangci.yml`). Start with the default set and add linters incrementally.

Your CI should run `golangci-lint run ./...` and fail if it exits non-zero.

At minimum, enable: `govet`, `errcheck`, `staticcheck`, `unused`, and `gosimple`. These catch the highest-value issues with near-zero false positives.

### 2. Type checking + vetting: go vet and go build

Go's compiler is already strict, but `go vet` catches issues the compiler allows: suspicious printf calls, struct tag errors, unreachable code, and copying of locks.

Your CI should run `go vet ./...` and `go build ./...` and fail on any error. If you are using golangci-lint with `govet` enabled, the `go vet` step is redundant but `go build` is still needed to verify compilation.

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

AI-generated Go frequently introduces unchecked errors, unused variables, incorrect struct tags, and occasionally hardcoded credentials. Large AI-generated PRs also tend to bundle unrelated changes.

- **golangci-lint** catches unchecked errors, dead code, inefficient patterns, and style violations across dozens of linters in one pass.
- **go vet + go build** catches compilation errors and subtle correctness issues the compiler alone misses.
- **TruffleHog** catches secrets that should never reach the repo.
- **PR size limits** force decomposition, making review tractable.

These checks are cheap, fast, and block the most common AI-generated defects before a human ever opens the PR.

## What this does NOT catch

Tier 0 catches formatting and obvious errors. It does not catch:

- Business logic bugs
- API contract drift between services
- Race conditions or goroutine leaks
- Security vulnerabilities beyond leaked secrets
- Missing or inadequate test coverage

See the [by-language reference](../quality-correctness-gates/by-language/go.md) for Tiers 1-3.

## Next steps

1. Read the [Go by-language page](../quality-correctness-gates/by-language/go.md) for testing, race detection, fuzzing, and architecture enforcement options.
2. Use the AI-assisted setup via `CLAUDE.md` in the repo root for guided configuration of higher tiers.
