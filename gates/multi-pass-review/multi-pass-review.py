#!/usr/bin/env python3
"""
Multi-pass AI code review script.

Runs a PR diff through an LLM three times with different review perspectives,
then aggregates findings. Based on the CodeX-Verify research showing that
diverse review perspectives improve accuracy from 32.8% to 72.4%.

Usage:
    # Review a diff file:
    python multi-pass-review.py --diff my-changes.diff

    # Review a GitHub PR:
    python multi-pass-review.py --pr 123 --repo owner/repo

    # Use a specific model:
    python multi-pass-review.py --diff my-changes.diff --model claude-sonnet-4-5-20250514

Requirements:
    pip install anthropic  # for Anthropic
    pip install openai     # for OpenAI
    pip install litellm    # for LiteLLM (100+ providers, with cost tracking)

Environment:
    ANTHROPIC_API_KEY=your-key   # for Anthropic
    OPENAI_API_KEY=your-key      # for OpenAI
    # LiteLLM uses the appropriate key for whichever provider you route to.
    # See https://docs.litellm.ai/docs/providers for provider-specific setup.

Providers:
    --provider anthropic   Use Anthropic API directly (default)
    --provider openai      Use OpenAI API directly
    --provider litellm     Use LiteLLM as a unified proxy. Supports Anthropic,
                           OpenAI, Google, Azure, AWS Bedrock, Ollama, and 100+
                           others. Automatically tracks per-call cost, which can
                           feed into the cost-per-accepted-change metric.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

# ── Review perspectives ──────────────────────────────────────────────
# Each perspective focuses on a different failure class.
# The CodeX-Verify research (arXiv 2511.16708) showed that four
# specialized agents improved accuracy from 32.8% to 72.4%.
# Three passes is a practical minimum.

PERSPECTIVES = {
    "correctness": {
        "name": "Correctness & Logic",
        "prompt": """You are a senior engineer reviewing this diff for correctness and logic errors.

Focus exclusively on:
- Does this code do what it claims to do?
- Off-by-one errors, boundary conditions, edge cases
- Null/undefined handling, empty collections, division by zero
- Thread safety, race conditions, deadlocks
- Broken invariants (e.g., idempotency violations, double-writes)
- Wrong assumptions about data shapes or upstream behavior

Do NOT comment on style, naming, performance, or security.
Only flag issues you are confident are actual bugs or logic errors.

For each issue found, provide:
- File and line (if identifiable from the diff)
- What the bug is
- Why it matters
- Suggested fix

If you find no issues, say "No correctness issues found." Do not invent problems.""",
    },
    "security": {
        "name": "Security & Scope",
        "prompt": """You are a security engineer reviewing this diff for vulnerabilities and scope violations.

Focus exclusively on:
- SQL injection, XSS, command injection, path traversal
- Hardcoded credentials, API keys, secrets
- Insufficient input validation at system boundaries
- Authentication/authorization gaps
- Data exposure (PII in logs, sensitive data in error messages)
- Dependency vulnerabilities (known-bad versions)
- Scope violations (code touching resources it should not)
- Permission escalation patterns

Do NOT comment on style, naming, performance, or general correctness.
Only flag issues you are confident are actual security risks.

For each issue found, provide:
- File and line (if identifiable from the diff)
- What the vulnerability is
- Severity (Critical / High / Medium / Low)
- Suggested fix

If you find no issues, say "No security issues found." Do not invent problems.""",
    },
    "performance": {
        "name": "Performance & Maintainability",
        "prompt": """You are a staff engineer reviewing this diff for performance problems and maintainability concerns.

Focus exclusively on:
- N+1 queries, unbounded loops over external data
- Missing pagination on database queries or API calls
- Resource leaks (unclosed connections, file handles, streams)
- Algorithmic inefficiency (O(n^2) where O(n) is possible)
- Unnecessary complexity, dead code, unreachable branches
- Code duplication that will cause maintenance drift
- Missing error handling on I/O operations
- Readability issues that will cause review burden on future changes

Do NOT comment on security, general correctness, or style preferences.
Only flag issues that will cause real performance problems or maintenance cost.

For each issue found, provide:
- File and line (if identifiable from the diff)
- What the problem is
- Expected impact (performance degradation, maintenance cost, etc.)
- Suggested fix

If you find no issues, say "No performance or maintainability issues found." Do not invent problems.""",
    },
}


# ── LLM call ─────────────────────────────────────────────────────────

def review_with_anthropic(diff: str, perspective: dict, model: str) -> str:
    try:
        import anthropic
    except ImportError:
        print("pip install anthropic", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"{perspective['prompt']}\n\n---\n\nDiff to review:\n\n{diff}",
            }
        ],
    )
    return response.content[0].text


def review_with_openai(diff: str, perspective: dict, model: str) -> str:
    try:
        import openai
    except ImportError:
        print("pip install openai", file=sys.stderr)
        sys.exit(1)

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=model,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"{perspective['prompt']}\n\n---\n\nDiff to review:\n\n{diff}",
            }
        ],
    )
    return response.choices[0].message.content


def review_with_litellm(diff: str, perspective: dict, model: str) -> str:
    """Use LiteLLM as a unified proxy — supports 100+ providers and tracks costs.

    LiteLLM also provides cost tracking per call via response_cost,
    which can feed directly into the cost-per-accepted-change metric.
    Set LITELLM_LOG=DEBUG to see per-call cost breakdowns.
    """
    try:
        import litellm
    except ImportError:
        print("pip install litellm", file=sys.stderr)
        sys.exit(1)

    response = litellm.completion(
        model=model,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"{perspective['prompt']}\n\n---\n\nDiff to review:\n\n{diff}",
            }
        ],
    )
    # Log cost if available (LiteLLM tracks this automatically)
    cost = getattr(response, "_hidden_params", {}).get("response_cost", None)
    if cost is not None:
        print(f"    Cost: ${cost:.4f}")
    return response.choices[0].message.content


# ── Main ─────────────────────────────────────────────────────────────

def get_diff(args) -> str:
    if args.diff:
        with open(args.diff) as f:
            return f.read()
    elif args.pr and args.repo:
        result = subprocess.run(
            ["gh", "pr", "diff", str(args.pr), "--repo", args.repo],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"Failed to fetch PR diff: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        return result.stdout
    else:
        print("Provide --diff <file> or --pr <number> --repo <owner/repo>", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Multi-pass AI code review")
    parser.add_argument("--diff", help="Path to a diff file")
    parser.add_argument("--pr", type=int, help="GitHub PR number")
    parser.add_argument("--repo", help="GitHub repo (owner/repo)")
    parser.add_argument("--model", default="claude-sonnet-4-5-20250514", help="Model to use")
    parser.add_argument("--provider", default="anthropic", choices=["anthropic", "openai", "litellm"])
    parser.add_argument("--output", default="review-results.md", help="Output file")
    args = parser.parse_args()

    diff = get_diff(args)

    if len(diff.strip()) == 0:
        print("Empty diff. Nothing to review.")
        return

    # Truncate very large diffs
    max_chars = 50000
    if len(diff) > max_chars:
        print(f"Diff is {len(diff)} chars, truncating to {max_chars} for review.")
        diff = diff[:max_chars] + "\n\n[... truncated ...]"

    providers = {
        "anthropic": review_with_anthropic,
        "openai": review_with_openai,
        "litellm": review_with_litellm,
    }
    review_fn = providers[args.provider]

    results = []
    for key, perspective in PERSPECTIVES.items():
        print(f"Pass {len(results) + 1}/3: {perspective['name']}...")
        result = review_fn(diff, perspective, args.model)
        results.append((perspective["name"], result))
        print(f"  Done.")

    # Write results
    with open(args.output, "w") as f:
        f.write(f"# Multi-Pass Code Review\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Model:** {args.model}\n")
        f.write(f"**Diff size:** {len(diff)} characters\n\n")
        f.write(f"---\n\n")

        issue_count = 0
        for name, result in results:
            f.write(f"## {name}\n\n")
            f.write(result)
            f.write("\n\n---\n\n")
            if "no " not in result.lower() or "issue" not in result.lower():
                issue_count += 1

        f.write(f"## Summary\n\n")
        f.write(f"Three review passes completed. See above for findings.\n")

    print(f"\nResults written to {args.output}")


if __name__ == "__main__":
    main()
