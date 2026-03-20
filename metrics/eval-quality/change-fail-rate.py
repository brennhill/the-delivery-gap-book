#!/usr/bin/env python3
"""
Change fail rate — what percentage of deployments cause production failure.

Formula: failed_deployments / total_deployments

This is a DORA core metric. The script supports:
1. GitHub Deployments API (if your team uses GitHub deployments)
2. GitHub Actions workflow runs (common proxy: failed workflow on main = failed deploy)
3. Manual input for teams with other deploy systems

Usage:
    # GitHub Actions (uses workflow runs on default branch as deploy proxy)
    python change-fail-rate.py --repo owner/repo --workflow deploy.yml

    # Manual input
    python change-fail-rate.py --total-deploys 120 --failed-deploys 8

    # JSON input
    echo '{"total_deploys": 120, "failed_deploys": 8}' | python change-fail-rate.py --json /dev/stdin
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta


def fetch_from_github_actions(repo: str, workflow: str, weeks: int) -> dict:
    """Use GitHub Actions workflow runs as a deployment proxy."""
    since = (datetime.now() - timedelta(weeks=weeks)).strftime("%Y-%m-%dT00:00:00Z")

    result = subprocess.run(
        [
            "gh", "api",
            f"repos/{repo}/actions/workflows/{workflow}/runs",
            "--paginate",
            "--jq", f'[.workflow_runs[] | select(.created_at >= "{since}" and .head_branch == "main")] | {{total: length, failed: [.[] | select(.conclusion == "failure")] | length, success: [.[] | select(.conclusion == "success")] | length}}',
        ],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
        return {
            "total_deploys": data["total"],
            "failed_deploys": data["failed"],
        }
    except (json.JSONDecodeError, KeyError):
        print("Could not parse workflow data. Check workflow name.", file=sys.stderr)
        sys.exit(1)


def fetch_from_deployments_api(repo: str, weeks: int) -> dict:
    """Use GitHub Deployments API."""
    since = (datetime.now() - timedelta(weeks=weeks)).strftime("%Y-%m-%dT00:00:00Z")

    result = subprocess.run(
        [
            "gh", "api",
            f"repos/{repo}/deployments",
            "--paginate",
            "--jq", f'[.[] | select(.created_at >= "{since}")] | length',
        ],
        capture_output=True, text=True,
    )
    total = int(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() else 0

    # Count failed deployment statuses
    result2 = subprocess.run(
        [
            "gh", "api",
            f"repos/{repo}/deployments",
            "--paginate",
            "--jq", f'[.[] | select(.created_at >= "{since}")] | .[].id',
        ],
        capture_output=True, text=True,
    )
    failed = 0
    if result2.returncode == 0:
        for deploy_id in result2.stdout.strip().split("\n"):
            if not deploy_id:
                continue
            status_result = subprocess.run(
                ["gh", "api", f"repos/{repo}/deployments/{deploy_id}/statuses", "--jq", ".[0].state"],
                capture_output=True, text=True,
            )
            if status_result.returncode == 0 and status_result.stdout.strip() in ("failure", "error"):
                failed += 1

    return {"total_deploys": total, "failed_deploys": failed}


def main():
    parser = argparse.ArgumentParser(description="Change fail rate (DORA metric)")
    parser.add_argument("--repo", help="GitHub repo (owner/repo)")
    parser.add_argument("--workflow", help="GitHub Actions workflow file (e.g., deploy.yml)")
    parser.add_argument("--weeks", type=int, default=4, help="Lookback (default: 4)")
    parser.add_argument("--total-deploys", type=int, help="Manual: total deployments")
    parser.add_argument("--failed-deploys", type=int, help="Manual: failed deployments")
    parser.add_argument("--json", help="Read from JSON file")
    args = parser.parse_args()

    if args.json:
        with open(args.json) as f:
            data = json.load(f)
        total = data["total_deploys"]
        failed = data["failed_deploys"]
    elif args.total_deploys is not None and args.failed_deploys is not None:
        total = args.total_deploys
        failed = args.failed_deploys
    elif args.repo and args.workflow:
        data = fetch_from_github_actions(args.repo, args.workflow, args.weeks)
        total = data["total_deploys"]
        failed = data["failed_deploys"]
    elif args.repo:
        data = fetch_from_deployments_api(args.repo, args.weeks)
        total = data["total_deploys"]
        failed = data["failed_deploys"]
    else:
        parser.error("Provide --repo (+ optional --workflow), --json, or --total-deploys + --failed-deploys")

    rate = (failed / total * 100) if total > 0 else 0

    print()
    print("=" * 50)
    print(" CHANGE FAIL RATE (DORA)")
    print("=" * 50)
    print()
    print(f"  Total deployments:     {total}")
    print(f"  Failed deployments:    {failed}")
    print(f"  Change fail rate:      {rate:.1f}%")
    print()

    # DORA benchmarks
    if rate <= 5:
        print("  Elite (DORA): < 5% change fail rate.")
    elif rate <= 10:
        print("  High (DORA): 5-10% change fail rate.")
    elif rate <= 15:
        print("  Medium (DORA): 10-15% change fail rate.")
    else:
        print("  Low (DORA): > 15% change fail rate.")
        print("  Investigate: are gates catching enough before deploy?")
    print()


if __name__ == "__main__":
    main()
