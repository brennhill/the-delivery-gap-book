"""Core review engine — sequential or parallel execution."""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from .perspectives import PERSPECTIVES
from .providers import PROVIDERS


def get_diff_from_file(path: str) -> str:
    with open(path) as f:
        return f.read()


def get_diff_from_pr(pr: int, repo: str) -> str:
    result = subprocess.run(
        ["gh", "pr", "diff", str(pr), "--repo", repo],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Failed to fetch PR diff: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def get_diff_from_stdin() -> str:
    return sys.stdin.read()


def run_review(
    diff: str,
    provider: str = "anthropic",
    model: str = "claude-sonnet-4-5-20250514",
    parallel: bool = False,
    perspectives: list[str] | None = None,
) -> list[dict]:
    """Run multi-pass review on a diff.

    Args:
        diff: The diff text to review.
        provider: LLM provider ("anthropic", "openai", "litellm").
        model: Model identifier.
        parallel: Run perspectives concurrently (faster, costs the same).
        perspectives: Which perspectives to run. Default: all three.

    Returns:
        List of result dicts with keys: perspective, result, cost.
    """
    if not diff.strip():
        return []

    # Truncate very large diffs
    max_chars = 50_000
    if len(diff) > max_chars:
        print(f"Diff is {len(diff)} chars, truncating to {max_chars}.")
        diff = diff[:max_chars] + "\n\n[... truncated ...]"

    review_fn = PROVIDERS[provider]

    # Select perspectives
    if perspectives:
        selected = {k: v for k, v in PERSPECTIVES.items() if k in perspectives}
    else:
        selected = PERSPECTIVES

    if parallel:
        return _run_parallel(diff, review_fn, model, selected)
    else:
        return _run_sequential(diff, review_fn, model, selected)


def _run_sequential(diff, review_fn, model, perspectives) -> list[dict]:
    results = []
    total = len(perspectives)
    for i, (key, perspective) in enumerate(perspectives.items(), 1):
        print(f"Pass {i}/{total}: {perspective['name']}...")
        result = review_fn(diff, perspective, model)
        if result.get("cost") is not None:
            print(f"  Cost: ${result['cost']:.4f}")
        print(f"  Done.")
        results.append(result)
    return results


def _run_parallel(diff, review_fn, model, perspectives) -> list[dict]:
    results = []
    total = len(perspectives)
    print(f"Running {total} perspectives in parallel...")

    with ThreadPoolExecutor(max_workers=total) as executor:
        futures = {}
        for key, perspective in perspectives.items():
            future = executor.submit(review_fn, diff, perspective, model)
            futures[future] = perspective["name"]

        for future in as_completed(futures):
            name = futures[future]
            try:
                result = future.result()
                cost_str = f" (${result['cost']:.4f})" if result.get("cost") else ""
                print(f"  Completed: {name}{cost_str}")
                results.append(result)
            except Exception as e:
                print(f"  Failed: {name} — {e}", file=sys.stderr)
                results.append({
                    "perspective": name,
                    "result": f"Error: {e}",
                    "cost": None,
                })

    return results


def format_markdown(results: list[dict], model: str, diff_len: int) -> str:
    """Format results as a markdown report."""
    lines = [
        "# Multi-Pass Code Review\n",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Model:** {model}",
        f"**Diff size:** {diff_len} characters",
        f"**Perspectives:** {len(results)}",
    ]

    total_cost = sum(r.get("cost") or 0 for r in results)
    if total_cost > 0:
        lines.append(f"**Total cost:** ${total_cost:.4f}")

    lines.append("\n---\n")

    for r in results:
        lines.append(f"## {r['perspective']}\n")
        lines.append(r["result"])
        lines.append("\n---\n")

    lines.append("## Summary\n")
    lines.append(f"{len(results)} review passes completed. See above for findings.\n")

    return "\n".join(lines)
