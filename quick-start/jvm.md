# Quick Start: JVM (Java / Kotlin)

> This guide covers Tier 0 (static analysis) only. It is a starting point, not complete verification. See the [by-language reference](../quality-correctness-gates/by-language/jvm.md) for higher tiers.

## What you need running in CI

### 1. Bug detection: SpotBugs (Java) or detekt (Kotlin)

**Java:** SpotBugs analyzes bytecode for common bug patterns — null dereferences, resource leaks, infinite loops, and concurrency errors. Add it as a build plugin and fail on any HIGH-confidence finding.

**Kotlin:** detekt is the equivalent for Kotlin. It catches code smells, complexity violations, and common bug patterns. Run `detekt --build-upon-default-config` and fail on any error.

**Both languages:** Add Error Prone as a compiler plugin. It catches bugs at compile time that neither SpotBugs nor detekt will find, such as incorrect equals/hashCode implementations and misuse of standard library APIs.

### 2. Type checking: the compiler

Java and Kotlin compilers are already strict. Ensure your CI runs a clean build (`./gradlew build` or `mvn compile`) with warnings treated as errors.

For Java, add `-Xlint:all -Werror` to compiler options. For Kotlin, add `-Werror` to treat all warnings as errors.

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

AI-generated JVM code frequently introduces null-safety issues, resource leaks (unclosed streams/connections), incorrect exception handling, and occasionally hardcoded credentials. Large AI-generated PRs also tend to bundle unrelated changes.

- **SpotBugs / detekt** catches null dereferences, resource leaks, dead code, and common bug patterns specific to each language.
- **Error Prone** catches correctness bugs at compile time that static analysis misses.
- **Compiler with strict warnings** catches deprecation usage, unchecked casts, and type issues.
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

See the [by-language reference](../quality-correctness-gates/by-language/jvm.md) for Tiers 1-3.

## Next steps

1. Read the [JVM by-language page](../quality-correctness-gates/by-language/jvm.md) for testing, mutation testing, and architecture enforcement options.
2. Use the AI-assisted setup via `CLAUDE.md` in the repo root for guided configuration of higher tiers.
