#!/usr/bin/env python3
"""
Defect escape rate — what percentage of bugs reach production vs caught pre-prod.

Formula: production_defects / (production_defects + pre_production_defects)

This requires issue tracker data. The script supports:
1. GitHub Issues with labels (e.g., "bug", "production", "pre-prod")
2. Manual JSON input for teams using Jira/Linear/other trackers

Usage:
    # GitHub Issues (requires labels like "bug" + "production" or "bug" + "found-in-review")
    python defect-escape-rate.py --repo owner/repo --weeks 4

    # Manual input
    python defect-escape-rate.py --production-bugs 5 --preprod-bugs 23

    # JSON input
    echo '{"production_bugs": 5, "preprod_bugs": 23}' | python defect-escape-rate.py --json /dev/stdin
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta


def fetch_from_github(repo: str, weeks: int) -> dict:
    """Count bugs by where they were found using GitHub issue labels."""
    since = (datetime.now() - timedelta(weeks=weeks)).strftime("%Y-%m-%d")

    # Production bugs: labeled "bug" AND ("production" or "prod" or "escaped")
    prod_result = subprocess.run(
        [
            "gh", "issue", "list", "--repo", repo,
            "--state", "all", "--limit", "500",
            "--label", "bug",
            "--search", f"created:>={since}",
            "--json", "number,title,labels",
        ],
        capture_output=True, text=True,
    )
    if prod_result.returncode != 0:
        print(f"Failed: {prod_result.stderr}", file=sys.stderr)
        sys.exit(1)

    issues = json.loads(prod_result.stdout)

    production = 0
    preprod = 0
    unclassified = 0

    prod_labels = {"production", "prod", "escaped", "incident", "hotfix", "post-release"}
    preprod_labels = {"found-in-review", "found-in-ci", "found-in-staging", "pre-prod", "preprod", "caught"}

    for issue in issues:
        label_names = {l["name"].lower() for l in issue.get("labels", [])}
        if label_names & prod_labels:
            production += 1
        elif label_names & preprod_labels:
            preprod += 1
        else:
            unclassified += 1

    return {
        "production_bugs": production,
        "preprod_bugs": preprod,
        "unclassified": unclassified,
        "total_bug_issues": len(issues),
    }


def calculate(production: int, preprod: int) -> dict:
    total = production + preprod
    if total == 0:
        return {"escape_rate": 0, "total": 0}
    return {
        "escape_rate": round(production / total * 100, 1),
        "production": production,
        "preprod": preprod,
        "total": total,
    }


def main():
    parser = argparse.ArgumentParser(description="Defect escape rate calculator")
    parser.add_argument("--repo", help="GitHub repo (owner/repo)")
    parser.add_argument("--weeks", type=int, default=4, help="Lookback (default: 4)")
    parser.add_argument("--production-bugs", type=int, help="Manual: production bug count")
    parser.add_argument("--preprod-bugs", type=int, help="Manual: pre-production bug count")
    parser.add_argument("--json", help="Read from JSON file")
    args = parser.parse_args()

    if args.json:
        with open(args.json) as f:
            data = json.load(f)
        production = data["production_bugs"]
        preprod = data["preprod_bugs"]
    elif args.production_bugs is not None and args.preprod_bugs is not None:
        production = args.production_bugs
        preprod = args.preprod_bugs
    elif args.repo:
        github_data = fetch_from_github(args.repo, args.weeks)
        production = github_data["production_bugs"]
        preprod = github_data["preprod_bugs"]
        if github_data["unclassified"] > 0:
            print(f"\n  Note: {github_data['unclassified']} bug issues have no")
            print(f"  production/pre-prod label and were excluded.")
            print(f"  Label your bugs with 'production' or 'found-in-review'")
            print(f"  for accurate tracking.\n")
    else:
        parser.error("Provide --repo, --json, or --production-bugs + --preprod-bugs")

    result = calculate(production, preprod)

    print()
    print("=" * 50)
    print(" DEFECT ESCAPE RATE")
    print("=" * 50)
    print()
    print(f"  Production bugs:       {result.get('production', 0)}")
    print(f"  Pre-production bugs:   {result.get('preprod', 0)}")
    print(f"  Total bugs found:      {result.get('total', 0)}")
    print()
    print(f"  Escape rate:           {result['escape_rate']}%")
    print()

    if result["escape_rate"] > 30:
        print("  Warning: High escape rate. Most bugs are reaching production.")
        print("  Your gates are not catching enough pre-merge.")
    elif result["escape_rate"] > 15:
        print("  Moderate. Some bugs escaping. Review gate coverage.")
    elif result["total"] > 0:
        print("  Healthy. Most bugs caught before production.")
    print()


if __name__ == "__main__":
    main()
