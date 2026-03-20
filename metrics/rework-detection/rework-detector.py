#!/usr/bin/env python3
"""
Rework detector — identifies accepted vs reworked changes from git history.

Scans the default branch merge history and classifies each change as
accepted, rework, or pending based on a 14-day observation window.

A change is "rework" if a subsequent merge to the default branch within
14 days matches any of these signals:
  1. Explicit git revert of the original commit
  2. Touches the same files AND has fix/hotfix/bugfix/patch in the message
  3. References the same ticket ID (JIRA-123, #123, ENG-123, etc.)
  4. Contains a Fixes: trailer pointing to the original SHA

A change is "accepted" if 14 days pass with no rework signal.
A change is "pending" if fewer than 14 days have elapsed.

Usage:
    # Scan current repo
    python rework-detector.py

    # Scan a GitHub repo
    python rework-detector.py --repo owner/repo

    # Custom window (default 14 days)
    python rework-detector.py --window 7

    # Output formats
    python rework-detector.py --json results.json
    python rework-detector.py --csv results.csv

Requirements:
    gh CLI (authenticated) for --repo mode
    git for local mode
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone


# ── Ticket ID patterns ───────────────────────────────────────────────

TICKET_PATTERNS = [
    re.compile(r"[A-Z]{2,10}-\d+"),          # JIRA/Linear: PROJ-123, ENG-456
    re.compile(r"#(\d+)"),                     # GitHub/GitLab: #123
    re.compile(r"(?:fixes|closes|resolves)\s+#(\d+)", re.IGNORECASE),
]

FIX_PATTERNS = re.compile(
    r"^(fix|hotfix|bugfix|patch|revert)[\s(:!/]",
    re.IGNORECASE | re.MULTILINE,
)

# Files to exclude from overlap detection — these are touched by many
# unrelated changes and create false positive rework signals.
IGNORE_FILES = {
    "README.md", "CHANGELOG.md", "CHANGES.md", "HISTORY.md",
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "Cargo.lock", "go.sum", "Gemfile.lock", "poetry.lock",
    "requirements.txt", "Pipfile.lock",
    ".gitignore", ".eslintrc.js", ".eslintrc.json", ".prettierrc",
    "tsconfig.json", "jest.config.js", "jest.config.ts",
    "Makefile", "Dockerfile", "docker-compose.yml",
}

IGNORE_PATTERNS = re.compile(
    r"(^\.github/|^docs/|^\.vscode/|manifest\.json$|\.lock$|\.sum$|"
    r"\.md$|\.txt$|\.yml$|\.yaml$|\.toml$|\.cfg$|\.ini$)",
    re.IGNORECASE,
)


def is_source_file(path: str) -> bool:
    """Check if a file is source code (not config, docs, or lock files)."""
    basename = path.split("/")[-1] if "/" in path else path
    if basename in IGNORE_FILES:
        return False
    if IGNORE_PATTERNS.search(path):
        return False
    return True


REVERT_PATTERN = re.compile(
    r'revert\s+"?(.+?)"?\s*$|^Revert\s+"(.+?)"',
    re.IGNORECASE | re.MULTILINE,
)

FIXES_TRAILER = re.compile(
    r"^Fixes:\s+([0-9a-f]{7,40})",
    re.MULTILINE,
)


def extract_ticket_ids(text: str) -> set:
    """Extract all ticket IDs from a commit message."""
    ids = set()
    for pattern in TICKET_PATTERNS:
        for match in pattern.finditer(text):
            ids.add(match.group(0).upper())
    return ids


def is_fix_message(text: str) -> bool:
    """Check if commit message indicates a fix/hotfix/patch."""
    return bool(FIX_PATTERNS.search(text))


def extract_fixes_sha(text: str) -> str | None:
    """Extract SHA from a Fixes: trailer."""
    m = FIXES_TRAILER.search(text)
    return m.group(1) if m else None


def is_revert_message(text: str) -> bool:
    """Check if commit message is an explicit revert."""
    return bool(REVERT_PATTERN.search(text))


# ── Git data fetching ────────────────────────────────────────────────

def get_merges_local(lookback_days: int) -> list[dict]:
    """Get merge commits from local git repo."""
    since = (datetime.now() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    result = subprocess.run(
        [
            "git", "log", "--first-parent", f"--since={since}",
            "--format=%H|%aI|%s|%b%x00",
        ],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"git log failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    commits = []
    for entry in result.stdout.split("\x00"):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split("|", 3)
        if len(parts) < 3:
            continue
        sha = parts[0]
        date_str = parts[1]
        subject = parts[2]
        body = parts[3] if len(parts) > 3 else ""
        message = f"{subject}\n{body}".strip()

        # Get files changed
        files_result = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", sha],
            capture_output=True, text=True,
        )
        files = set(files_result.stdout.strip().split("\n")) if files_result.stdout.strip() else set()

        commits.append({
            "sha": sha,
            "short_sha": sha[:10],
            "date": datetime.fromisoformat(date_str),
            "subject": subject,
            "message": message,
            "files": files,
            "ticket_ids": extract_ticket_ids(message),
            "is_fix": is_fix_message(message),
            "is_revert": is_revert_message(message),
            "fixes_sha": extract_fixes_sha(message),
        })

    return commits


def get_merges_github(repo: str, lookback_days: int) -> list[dict]:
    """Get merged PRs from GitHub API."""
    since = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    result = subprocess.run(
        [
            "gh", "pr", "list", "--repo", repo,
            "--state", "merged", "--limit", "500",
            "--search", f"merged:>={since[:10]}",
            "--json", "number,title,mergedAt,files,mergeCommit",
        ],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"gh pr list failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    prs = json.loads(result.stdout)
    commits = []

    for pr in prs:
        title = pr.get("title", "")
        sha = pr.get("mergeCommit", {}).get("oid", "")
        merged_at = pr.get("mergedAt", "")
        files = set(f.get("path", "") for f in pr.get("files", []))

        # Also fetch commit message body for trailers
        body = ""
        if sha:
            body_result = subprocess.run(
                ["gh", "api", f"repos/{repo}/commits/{sha}", "--jq", ".commit.message"],
                capture_output=True, text=True,
            )
            if body_result.returncode == 0:
                body = body_result.stdout.strip()

        message = f"{title}\n{body}".strip()

        commits.append({
            "sha": sha,
            "short_sha": sha[:10] if sha else f"PR#{pr['number']}",
            "pr_number": pr["number"],
            "date": datetime.fromisoformat(merged_at.replace("Z", "+00:00")) if merged_at else datetime.now(timezone.utc),
            "subject": title,
            "message": message,
            "files": files,
            "ticket_ids": extract_ticket_ids(message),
            "is_fix": is_fix_message(message),
            "is_revert": is_revert_message(message),
            "fixes_sha": extract_fixes_sha(message),
        })

    return commits


# ── Rework detection ─────────────────────────────────────────────────

def detect_rework(commits: list[dict], window_days: int) -> list[dict]:
    """Classify each commit as accepted, rework, or pending."""
    now = datetime.now(timezone.utc)
    # Ensure all dates are timezone-aware
    for c in commits:
        if c["date"].tzinfo is None:
            c["date"] = c["date"].replace(tzinfo=timezone.utc)

    # Sort oldest first
    commits.sort(key=lambda c: c["date"])

    results = []

    for i, original in enumerate(commits):
        age_days = (now - original["date"]).days
        rework_signals = []

        # Look at all later commits within the window
        for j in range(i + 1, len(commits)):
            candidate = commits[j]
            delta_days = (candidate["date"] - original["date"]).days

            if delta_days > window_days:
                break

            # Signal 1: Explicit revert
            if candidate["is_revert"] and (
                original["short_sha"] in candidate["message"]
                or original["subject"] in candidate["message"]
            ):
                rework_signals.append(f"Reverted by {candidate['short_sha']}")
                continue

            # Signal 2: Fixes: trailer pointing to this commit
            if candidate["fixes_sha"] and original["sha"].startswith(candidate["fixes_sha"]):
                rework_signals.append(f"Fixes: trailer in {candidate['short_sha']}")
                continue

            # Signal 3: Same ticket ID AND is a fix
            if candidate["ticket_ids"] and original["ticket_ids"]:
                shared = candidate["ticket_ids"] & original["ticket_ids"]
                if shared and candidate["is_fix"]:
                    rework_signals.append(
                        f"Same ticket {', '.join(shared)} fixed by {candidate['short_sha']}"
                    )
                    continue

            # Signal 4: Same SOURCE files AND is a fix
            # Only count source code files (not README, configs, lock files)
            # The fix must be *about* the original change: >50% of the fix's
            # source files must overlap with the original's source files.
            # This prevents a single fix to a shared utility from marking
            # every prior commit that also touched that utility.
            if candidate["is_fix"] and candidate["files"] and original["files"]:
                orig_src = {f for f in original["files"] if is_source_file(f)}
                cand_src = {f for f in candidate["files"] if is_source_file(f)}
                overlap = orig_src & cand_src
                if len(cand_src) > 0 and len(overlap) / len(cand_src) > 0.5:
                    rework_signals.append(
                        f"Fix {candidate['short_sha']} touches same source files: {', '.join(list(overlap)[:3])}"
                    )
                    continue

        # Classify
        if age_days < window_days:
            status = "pending"
        elif rework_signals:
            status = "rework"
        else:
            status = "accepted"

        results.append({
            "sha": original["short_sha"],
            "date": original["date"].strftime("%Y-%m-%d"),
            "subject": original["subject"][:80],
            "status": status,
            "age_days": age_days,
            "signals": rework_signals,
            "ticket_ids": list(original["ticket_ids"]),
            "files_changed": len(original["files"]),
        })

    return results


# ── Output ───────────────────────────────────────────────────────────

def print_report(results: list[dict], window_days: int):
    accepted = [r for r in results if r["status"] == "accepted"]
    rework = [r for r in results if r["status"] == "rework"]
    pending = [r for r in results if r["status"] == "pending"]

    print()
    print("=" * 60)
    print(f" REWORK DETECTION REPORT ({window_days}-day window)")
    print("=" * 60)
    print()
    print(f"  Accepted:  {len(accepted)}")
    print(f"  Rework:    {len(rework)}")
    print(f"  Pending:   {len(pending)} (< {window_days} days old)")
    print()

    total_classifiable = len(accepted) + len(rework)
    if total_classifiable > 0:
        rate = len(rework) / total_classifiable * 100
        print(f"  Rework rate: {rate:.1f}%")
    else:
        print("  Rework rate: N/A (no changes old enough to classify)")
    print()

    if rework:
        print("  REWORKED CHANGES:")
        print("  " + "-" * 56)
        for r in rework:
            print(f"  {r['sha']}  {r['date']}  {r['subject'][:50]}")
            for signal in r["signals"]:
                print(f"    -> {signal}")
        print()

    if pending:
        print(f"  PENDING ({len(pending)} changes awaiting {window_days}-day window):")
        print("  " + "-" * 56)
        for r in pending:
            days_left = window_days - r["age_days"]
            print(f"  {r['sha']}  {r['date']}  ({days_left}d left)  {r['subject'][:45]}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Detect rework in git merge history")
    parser.add_argument("--repo", help="GitHub repo (owner/repo). Omit for local git.")
    parser.add_argument("--window", type=int, default=14, help="Observation window in days (default: 14)")
    parser.add_argument("--lookback", type=int, default=45, help="How far back to scan (default: 45 days)")
    parser.add_argument("--json", help="Write results to JSON file")
    parser.add_argument("--csv", help="Write results to CSV file")
    args = parser.parse_args()

    print(f"Scanning {'GitHub ' + args.repo if args.repo else 'local repo'}...")
    print(f"Window: {args.window} days, lookback: {args.lookback} days")

    if args.repo:
        commits = get_merges_github(args.repo, args.lookback)
    else:
        commits = get_merges_local(args.lookback)

    if not commits:
        print("No commits found in the lookback period.")
        return

    print(f"Found {len(commits)} commits to analyze.")

    results = detect_rework(commits, args.window)
    print_report(results, args.window)

    if args.json:
        with open(args.json, "w") as f:
            json.dump(results, f, indent=2)
        print(f"  Results written to {args.json}")

    if args.csv:
        import csv
        with open(args.csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "sha", "date", "subject", "status", "age_days",
                "signals", "ticket_ids", "files_changed",
            ])
            writer.writeheader()
            for r in results:
                row = dict(r)
                row["signals"] = "; ".join(r["signals"])
                row["ticket_ids"] = ", ".join(r["ticket_ids"])
                writer.writerow(row)
        print(f"  Results written to {args.csv}")


if __name__ == "__main__":
    main()
