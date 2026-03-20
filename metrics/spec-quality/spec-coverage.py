#!/usr/bin/env python3
"""
Spec coverage — measures what percentage of merged PRs have a linked spec.

Scans PR descriptions for spec links: URLs, ticket IDs (JIRA-123, #123, ENG-456),
or a populated spec-link field. PRs without a valid spec link count as unspec'd.

Usage:
    python spec-coverage.py --repo owner/repo
    python spec-coverage.py --repo owner/repo --weeks 4
    python spec-coverage.py --repo owner/repo --json results.json
"""

import argparse
import json
import re
import subprocess
import sys


TICKET_PATTERNS = [
    re.compile(r"[A-Z]{2,10}-\d+"),           # JIRA/Linear: PROJ-123
    re.compile(r"#\d+"),                        # GitHub: #123
]

URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)

PLACEHOLDER_PATTERNS = re.compile(
    r"(^|\s)(tbd|pending|todo|n/a|none|wip)(\s|$)",
    re.IGNORECASE,
)

SPEC_FIELD_PATTERNS = re.compile(
    r"(spec|design|rfc|adr|requirement|proposal)\s*(link|url|doc)?\s*[:=]\s*(\S+)",
    re.IGNORECASE,
)


def has_valid_spec(body: str) -> dict:
    """Check if a PR body contains a valid spec link."""
    if not body:
        return {"has_spec": False, "reason": "empty description"}

    # Check for placeholder values
    if PLACEHOLDER_PATTERNS.search(body):
        # Only if the placeholder is near a spec-related field
        spec_field = SPEC_FIELD_PATTERNS.search(body)
        if spec_field and PLACEHOLDER_PATTERNS.search(spec_field.group(3)):
            return {"has_spec": False, "reason": "placeholder spec link"}

    # Check for explicit spec field with a URL
    spec_field = SPEC_FIELD_PATTERNS.search(body)
    if spec_field:
        value = spec_field.group(3)
        if URL_PATTERN.match(value):
            return {"has_spec": True, "reason": f"spec field: {value[:60]}"}

    # Check for ticket IDs
    for pattern in TICKET_PATTERNS:
        match = pattern.search(body)
        if match:
            return {"has_spec": True, "reason": f"ticket: {match.group(0)}"}

    # Check for any URL (generous — assumes linked docs are specs)
    url_match = URL_PATTERN.search(body)
    if url_match:
        url = url_match.group(0)
        # Filter out common non-spec URLs
        if not any(skip in url.lower() for skip in ["github.com/pulls", "codecov.io", "circleci.com", "travis-ci.org"]):
            return {"has_spec": True, "reason": f"url: {url[:60]}"}

    return {"has_spec": False, "reason": "no spec link found"}


def fetch_prs(repo: str, weeks: int) -> list:
    from datetime import datetime, timedelta
    since = (datetime.now() - timedelta(weeks=weeks)).strftime("%Y-%m-%d")
    result = subprocess.run(
        [
            "gh", "pr", "list", "--repo", repo,
            "--state", "merged", "--limit", "500",
            "--search", f"merged:>={since}",
            "--json", "number,title,body,mergedAt,labels",
        ],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"gh pr list failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description="Spec coverage scanner")
    parser.add_argument("--repo", required=True, help="GitHub repo (owner/repo)")
    parser.add_argument("--weeks", type=int, default=4, help="Lookback period (default: 4)")
    parser.add_argument("--json", help="Write results to JSON")
    args = parser.parse_args()

    prs = fetch_prs(args.repo, args.weeks)
    if not prs:
        print("No merged PRs found.")
        return

    results = []
    for pr in prs:
        body = pr.get("body", "") or ""
        check = has_valid_spec(body)
        results.append({
            "number": pr["number"],
            "title": pr["title"][:60],
            "has_spec": check["has_spec"],
            "reason": check["reason"],
        })

    spec_count = sum(1 for r in results if r["has_spec"])
    no_spec_count = len(results) - spec_count
    coverage = spec_count / len(results) * 100 if results else 0

    print()
    print("=" * 50)
    print(f" SPEC COVERAGE — {args.repo}")
    print("=" * 50)
    print()
    print(f"  Total merged PRs:     {len(results)}")
    print(f"  With spec link:       {spec_count}")
    print(f"  Without spec link:    {no_spec_count}")
    print(f"  Coverage:             {coverage:.1f}%")
    print()

    if no_spec_count > 0:
        print("  UNSPEC'D PRs:")
        print("  " + "-" * 46)
        for r in results:
            if not r["has_spec"]:
                print(f"  #{r['number']}  {r['title'][:45]}  ({r['reason']})")
        print()

    if args.json:
        with open(args.json, "w") as f:
            json.dump({
                "repo": args.repo,
                "weeks": args.weeks,
                "total": len(results),
                "with_spec": spec_count,
                "without_spec": no_spec_count,
                "coverage_pct": round(coverage, 1),
                "prs": results,
            }, f, indent=2)
        print(f"  Results written to {args.json}")


if __name__ == "__main__":
    main()
