#!/usr/bin/env python3
"""
Reviewer-minutes per accepted change — how long humans spend reviewing each change.

Pulls review timestamps from GitHub API to compute time between
review-requested and approved for each merged PR.

Usage:
    python reviewer-minutes.py --repo owner/repo
    python reviewer-minutes.py --repo owner/repo --weeks 4
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone


def fetch_prs(repo: str, weeks: int) -> list:
    since = (datetime.now() - timedelta(weeks=weeks)).strftime("%Y-%m-%d")
    result = subprocess.run(
        [
            "gh", "pr", "list", "--repo", repo,
            "--state", "merged", "--limit", "200",
            "--search", f"merged:>={since}",
            "--json", "number,title,createdAt,mergedAt",
        ],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def get_review_time(repo: str, pr_number: int) -> float | None:
    """Get review duration in minutes for a PR."""
    result = subprocess.run(
        [
            "gh", "api",
            f"repos/{repo}/pulls/{pr_number}/reviews",
            "--jq", '[.[] | select(.state == "APPROVED" or .state == "CHANGES_REQUESTED") | .submitted_at] | sort | first',
        ],
        capture_output=True, text=True,
    )
    first_review = None
    if result.returncode == 0 and result.stdout.strip() and result.stdout.strip() != "null":
        try:
            first_review = datetime.fromisoformat(result.stdout.strip().replace("Z", "+00:00"))
        except ValueError:
            pass

    # Get when review was requested (use PR created as proxy)
    result2 = subprocess.run(
        [
            "gh", "api",
            f"repos/{repo}/pulls/{pr_number}",
            "--jq", ".created_at",
        ],
        capture_output=True, text=True,
    )
    created = None
    if result2.returncode == 0 and result2.stdout.strip():
        try:
            created = datetime.fromisoformat(result2.stdout.strip().replace("Z", "+00:00"))
        except ValueError:
            pass

    if first_review and created:
        delta = (first_review - created).total_seconds() / 60
        # Cap at 7 days (anything longer is probably not active review time)
        return min(delta, 7 * 24 * 60)

    return None


def main():
    parser = argparse.ArgumentParser(description="Reviewer-minutes per accepted change")
    parser.add_argument("--repo", required=True, help="GitHub repo (owner/repo)")
    parser.add_argument("--weeks", type=int, default=4, help="Lookback (default: 4)")
    parser.add_argument("--json", help="Write results to JSON")
    args = parser.parse_args()

    prs = fetch_prs(args.repo, args.weeks)
    if not prs:
        print("No merged PRs found.")
        return

    review_times = []
    for i, pr in enumerate(prs):
        print(f"  Scanning PR #{pr['number']} ({i+1}/{len(prs)})...", end="\r")
        minutes = get_review_time(args.repo, pr["number"])
        if minutes is not None:
            review_times.append({
                "number": pr["number"],
                "title": pr["title"][:50],
                "review_minutes": round(minutes, 1),
            })

    print(" " * 60)

    if not review_times:
        print("No review data found.")
        return

    times = [r["review_minutes"] for r in review_times]
    times.sort()
    median = times[len(times) // 2]
    mean = sum(times) / len(times)
    p95 = times[int(len(times) * 0.95)] if len(times) >= 20 else times[-1]

    print()
    print("=" * 50)
    print(f" REVIEWER-MINUTES — {args.repo}")
    print("=" * 50)
    print()
    print(f"  PRs with review data:  {len(review_times)}")
    print(f"  Median review time:    {median:.0f} minutes")
    print(f"  Mean review time:      {mean:.0f} minutes")
    print(f"  P95 review time:       {p95:.0f} minutes")
    print()

    if median > 60:
        print("  Warning: Median review exceeds 60 minutes.")
        print("  SmartBear/Cisco research shows effectiveness drops")
        print("  sharply after 60 minutes of continuous review.")
    print()

    # Show slowest reviews
    slowest = sorted(review_times, key=lambda r: r["review_minutes"], reverse=True)[:5]
    if slowest:
        print("  Slowest reviews:")
        print("  " + "-" * 46)
        for r in slowest:
            hours = r["review_minutes"] / 60
            print(f"  #{r['number']}  {r['title'][:40]}  ({hours:.1f}h)")
        print()

    if args.json:
        with open(args.json, "w") as f:
            json.dump({
                "repo": args.repo,
                "weeks": args.weeks,
                "prs_with_data": len(review_times),
                "median_minutes": round(median, 1),
                "mean_minutes": round(mean, 1),
                "p95_minutes": round(p95, 1),
                "prs": review_times,
            }, f, indent=2)
        print(f"  Results written to {args.json}")


if __name__ == "__main__":
    main()
