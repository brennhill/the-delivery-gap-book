"""CLI entry point for code-reviewers."""

import argparse
import sys

from .reviewer import (
    get_diff_from_file,
    get_diff_from_pr,
    get_diff_from_stdin,
    run_review,
    format_markdown,
)


def main():
    parser = argparse.ArgumentParser(
        prog="code-reviewers",
        description="Multi-pass AI code review with three specialized perspectives.",
    )
    parser.add_argument("--diff", help="Path to a diff file")
    parser.add_argument("--pr", type=int, help="GitHub PR number")
    parser.add_argument("--repo", help="GitHub repo (owner/repo)")
    parser.add_argument("--model", default="claude-sonnet-4-5-20250514", help="Model to use")
    parser.add_argument(
        "--provider", default="anthropic",
        choices=["anthropic", "openai", "litellm"],
        help="LLM provider",
    )
    parser.add_argument(
        "--parallel", action="store_true",
        help="Run all perspectives concurrently (faster, same cost)",
    )
    parser.add_argument(
        "--perspectives",
        nargs="+",
        choices=["correctness", "security", "performance"],
        help="Which perspectives to run (default: all three)",
    )
    parser.add_argument("--output", default="review-results.md", help="Output file")
    args = parser.parse_args()

    # Get the diff
    if args.diff:
        diff = get_diff_from_file(args.diff)
    elif args.pr and args.repo:
        diff = get_diff_from_pr(args.pr, args.repo)
    elif not sys.stdin.isatty():
        diff = get_diff_from_stdin()
    else:
        parser.error("Provide --diff <file>, --pr <number> --repo <owner/repo>, or pipe a diff to stdin")

    if not diff.strip():
        print("Empty diff. Nothing to review.")
        return

    mode = "parallel" if args.parallel else "sequential"
    print(f"Mode: {mode} | Model: {args.model} | Provider: {args.provider}")

    results = run_review(
        diff=diff,
        provider=args.provider,
        model=args.model,
        parallel=args.parallel,
        perspectives=args.perspectives,
    )

    report = format_markdown(results, args.model, len(diff))

    with open(args.output, "w") as f:
        f.write(report)

    print(f"\nResults written to {args.output}")


if __name__ == "__main__":
    main()
