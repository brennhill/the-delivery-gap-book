# Cost Efficiency — Token and Context Optimization

AI-assisted development has a cost dimension that most teams ignore until the invoice arrives. Every tool call, every file read, every test output consumes tokens. A 30-minute coding session can burn 100K+ tokens on command output alone — most of it noise the model never needed.

Cost efficiency is not about spending less. It is about spending tokens on signal instead of noise. The Verification Triangle's cost vertex depends on this: cost per accepted change includes model spend, and model spend scales with token consumption.

---

## Token Compression

### RTK (Rust Token Killer)

| | |
|---|---|
| **What it does** | CLI proxy that filters and compresses command outputs before they reach your LLM context. Smart filtering, grouping, truncation, and deduplication across 100+ commands (git, cargo, npm, ls, test runners, build tools). |
| **Savings** | 60-90% token reduction. A typical 30-minute Claude Code session drops from ~118K tokens to ~24K. |
| **How it works** | Single Rust binary, no dependencies. Runs as a transparent proxy — either manual (`rtk git status`) or automatic via Claude Code hooks that rewrite Bash commands in real time. |
| **Open source** | Yes (Apache 2.0) |
| **URL** | https://github.com/rtk-ai/rtk |

Token savings compound. If your team runs 50 agent sessions per day and each session saves 80K tokens, that is 4M tokens per day — real money at frontier model pricing, and real context window budget recovered for actual reasoning.

---

## Context Quality

### Context7

| | |
|---|---|
| **What it does** | MCP server and CLI that fetches up-to-date, version-specific documentation and code examples from library source repos. Replaces hallucinated API references with real ones. |
| **Why it matters** | LLMs hallucinate package APIs constantly — calling functions that do not exist, using deprecated signatures, inventing parameters. Context7 anchors generation in current documentation, reducing rework from hallucinated code. |
| **How it works** | Integrates with Claude Code, Cursor, and other MCP-compatible tools. The agent queries documentation as needed rather than relying on stale training data. |
| **Open source** | Yes (Apache 2.0) |
| **URL** | https://github.com/upstash/context7 |

Accurate documentation context reduces iteration cycles. Every hallucinated API call that reaches code review is a round-trip the reviewer and the agent both wasted. Context7 prevents the hallucination rather than catching it after the fact.

---

## Agent Code Navigation

### Serena

| | |
|---|---|
| **What it does** | MCP server providing semantic code retrieval, editing, and refactoring tools for coding agents. Operates at the symbol level — function definitions, class hierarchies, references — rather than text matching. |
| **Why it matters** | Agents navigating large codebases by grepping for strings waste tokens on false matches and miss semantic relationships. Serena gives agents IDE-level navigation (go-to-definition, find-references, safe rename) without an IDE. |
| **How it works** | MCP server compatible with Claude Code and other MCP clients. Agents discover symbols, understand relationships, and make targeted edits instead of reading entire files. |
| **Open source** | Yes (Apache 2.0) |
| **URL** | https://github.com/oraios/serena |

Better code navigation means fewer files read, fewer tokens consumed, and fewer wrong-file edits that trigger rework. This is cost efficiency through precision rather than compression.

---

## The Cost Efficiency Stack

These tools are complementary:

| Layer | Tool | What it saves |
|-------|------|--------------|
| **Output compression** | RTK | Tokens wasted on verbose command output |
| **Input quality** | Context7 | Iterations wasted on hallucinated APIs |
| **Navigation precision** | Serena | Tokens wasted on broad file reads and grep misses |

None of these replace verification. They reduce the cost of the verification loop — fewer tokens per iteration, fewer iterations per feature, lower cost per accepted change.
