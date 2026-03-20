#!/usr/bin/env python3
"""
Machine catch rate — what percentage of defects are caught by automated gates
versus discovered by human reviewers.

Scans GitHub PRs for:
- Machine catches: CI check failures (status checks that failed then passed after fix)
- Human catches: review comments requesting changes

Formula: machine_catches / (machine_catches + human_catches)

Usage:
    python machine-catch-rate.py --repo owner/repo
    python machine-catch-rate.py --repo owner/repo --weeks 4
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta


def fetch_prs(repo: str, weeks: int) -> list:
    since = (datetime.now() - timedelta(weeks=weeks)).strftime("%Y-%m-%d")
    result = subprocess.run(
        [
            "gh", "pr", "list", "--repo", repo,
            "--state", "merged", "--limit", "200",
            "--search", f"merged:>={since}",
            "--json", "number,title",
        ],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"gh pr list failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def get_pr_checks(repo: str, pr_number: int) -> dict:
    """Count CI failures and review comments for a PR."""
    # Get check runs
    checks_result = subprocess.run(
        ["gh", "pr", "checks", str(pr_number), "--repo", repo, "--json", "name,state"],
        capture_output=True, text=True,
    )
    ci_failures = 0
    if checks_result.returncode == 0:
        try:
            checks = json.loads(checks_result.stdout)
            # A check that exists means it ran; we count based on whether
            # the PR had failing checks that were later fixed (re-run and passed)
            ci_failures = sum(1 for c in checks if c.get("state") == "FAILURE")
        except json.JSONDecodeError:
            pass

    # Get review comments (human catches)
    reviews_result = subprocess.run(
        [
            "gh", "api",
            f"repos/{repo}/pulls/{pr_number}/reviews",
            "--jq", '[.[] | select(.state == "CHANGES_REQUESTED")] | length',
        ],
        capture_output=True, text=True,
    )
    human_catches = 0
    if reviews_result.returncode == 0 and reviews_result.stdout.strip():
        try:
            human_catches = int(reviews_result.stdout.strip())
        except ValueError:
            pass

    # Also count review comments (inline feedback)
    comments_result = subprocess.run(
        [
            "gh", "api",
            f"repos/{repo}/pulls/{pr_number}/comments",
            "--jq", "length",
        ],
        capture_output=True, text=True,
    )
    review_comments = 0
    if comments_result.returncode == 0 and comments_result.stdout.strip():
        try:
            review_comments = int(comments_result.stdout.strip())
        except ValueError:
            pass

    return {
        "ci_failures": ci_failures,
        "change_requests": human_catches,
        "review_comments": review_comments,
    }


def main():
    parser = argparse.ArgumentParser(description="Machine catch rate estimator")
    parser.add_argument("--repo", required=True, help="GitHub repo (owner/repo)")
    parser.add_argument("--weeks", type=int, default=4, help="Lookback (default: 4)")
    parser.add_argument("--json", help="Write results to JSON")
    args = parser.parse_args()

    prs = fetch_prs(args.repo, args.weeks)
    if not prs:
        print("No merged PRs found.")
        return

    total_machine = 0
    total_human = 0
    pr_details = []

    for i, pr in enumerate(prs):
        print(f"  Scanning PR #{pr['number']} ({i+1}/{len(prs)})...", end="\r")
        checks = get_pr_checks(args.repo, pr["number"])
        machine = checks["ci_failures"]
        human = checks["change_requests"] + min(checks["review_comments"], 3)  # cap inline comments
        total_machine += machine
        total_human += human
        pr_details.append({
            "number": pr["number"],
            "title": pr["title"][:50],
            "machine_catches": machine,
            "human_catches": human,
        })

    print(" " * 60)  # clear progress line

    total = total_machine + total_human
    rate = (total_machine / total * 100) if total > 0 else 0

    print()
    print("=" * 50)
    print(f" MACHINE CATCH RATE — {args.repo}")
    print("=" * 50)
    print()
    print(f"  Machine catches (CI failures):     {total_machine}")
    print(f"  Human catches (review feedback):    {total_human}")
    print(f"  Total catches:                      {total}")
    print()
    print(f"  Machine catch rate:                 {rate:.1f}%")
    print()

    if rate < 20:
        print("  Warning: Very low machine catch rate.")
        print("  Your automated gates are catching almost nothing.")
        print("  Human reviewers are doing all the defect detection work.")
    elif rate < 50:
        print("  Your gates are catching some issues but humans are")
        print("  still finding most problems. Add more gate tiers.")
    else:
        print("  Healthy: machines catch more than humans.")
        print("  Your gates are absorbing review burden effectively.")
    print()

    if args.json:
        with open(args.json, "w") as f:
            json.dump({
                "repo": args.repo,
                "weeks": args.weeks,
                "machine_catches": total_machine,
                "human_catches": total_human,
                "machine_catch_rate_pct": round(rate, 1),
                "prs": pr_details,
            }, f, indent=2)
        print(f"  Results written to {args.json}")


if __name__ == "__main__":
    main()
