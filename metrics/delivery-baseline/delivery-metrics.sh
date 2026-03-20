#!/usr/bin/env bash
#
# delivery-metrics.sh — Compute the four baseline metrics from git history.
#
# Produces a weekly scorecard from your repository data without
# requiring a commercial engineering intelligence platform.
#
# Usage:
#   ./delivery-metrics.sh                    # defaults: 4 weeks, current repo
#   ./delivery-metrics.sh --weeks 8          # look back 8 weeks
#   ./delivery-metrics.sh --repo owner/repo  # use GitHub API (requires gh CLI)
#
# Output: prints scorecard to stdout, writes CSV to delivery-metrics.csv
#
# What it measures:
#   1. Merged PRs (proxy for accepted changes)
#   2. Reverted PRs (proxy for rework)
#   3. Rework rate (reverts / merged)
#   4. Median PR cycle time (open → merge)
#
# What it does NOT measure (requires manual input):
#   - Reviewer-minutes per accepted change (estimate from review timestamps)
#   - Defect escape rate (requires issue tracker data)
#   - Cost per accepted change (requires cost inputs — see cost-calculator.py)
#
# Requirements: gh CLI (authenticated), jq, awk

set -euo pipefail

WEEKS="${1:-4}"
REPO=""

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --weeks) WEEKS="$2"; shift 2 ;;
        --repo) REPO="$2"; shift 2 ;;
        *) shift ;;
    esac
done

SINCE=$(date -v-"${WEEKS}"w +%Y-%m-%d 2>/dev/null || date -d "${WEEKS} weeks ago" +%Y-%m-%d)
REPO_FLAG=""
if [[ -n "$REPO" ]]; then
    REPO_FLAG="--repo $REPO"
fi

echo "═══════════════════════════════════════════════════"
echo " Delivery Metrics — last ${WEEKS} weeks (since ${SINCE})"
echo "═══════════════════════════════════════════════════"
echo ""

# ── Merged PRs ────────────────────────────────────────
echo "Fetching merged PRs..."
MERGED_DATA=$(gh pr list $REPO_FLAG --state merged --search "merged:>=${SINCE}" --limit 500 \
    --json number,title,createdAt,mergedAt,additions,deletions 2>/dev/null || echo "[]")

MERGED_COUNT=$(echo "$MERGED_DATA" | jq 'length')
echo "  Merged PRs: $MERGED_COUNT"

# ── Reverted PRs (search for "revert" in titles) ─────
echo "Checking for reverts..."
REVERT_COUNT=$(echo "$MERGED_DATA" | jq '[.[] | select(.title | test("revert|rollback|undo"; "i"))] | length')
echo "  Reverted PRs: $REVERT_COUNT"

# ── Rework rate ───────────────────────────────────────
if [[ "$MERGED_COUNT" -gt 0 ]]; then
    REWORK_RATE=$(echo "scale=1; $REVERT_COUNT * 100 / $MERGED_COUNT" | bc)
else
    REWORK_RATE="0"
fi
echo "  Rework rate: ${REWORK_RATE}%"

# ── PR cycle time (median hours from open to merge) ──
echo "Computing cycle times..."
CYCLE_TIMES=$(echo "$MERGED_DATA" | jq -r '.[] |
    (((.mergedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 3600) |
    floor' 2>/dev/null | sort -n)

if [[ -n "$CYCLE_TIMES" ]]; then
    TOTAL_PRS=$(echo "$CYCLE_TIMES" | wc -l | tr -d ' ')
    MEDIAN_INDEX=$(( (TOTAL_PRS + 1) / 2 ))
    MEDIAN_HOURS=$(echo "$CYCLE_TIMES" | sed -n "${MEDIAN_INDEX}p")
    echo "  Median cycle time: ${MEDIAN_HOURS} hours"
else
    MEDIAN_HOURS="N/A"
    echo "  Median cycle time: N/A"
fi

# ── Average PR size ───────────────────────────────────
AVG_SIZE=$(echo "$MERGED_DATA" | jq 'if length > 0 then ([.[] | .additions + .deletions] | add / length | floor) else 0 end')
echo "  Average PR size: ${AVG_SIZE} lines changed"

# ── Accepted changes (merged minus reverts) ───────────
ACCEPTED=$((MERGED_COUNT - REVERT_COUNT))
echo ""
echo "  Accepted changes: $ACCEPTED"

# ── Output ────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════"
echo " Weekly Scorecard"
echo "═══════════════════════════════════════════════════"
echo ""
printf "  %-35s %s\n" "Merged PRs:" "$MERGED_COUNT"
printf "  %-35s %s\n" "Reverted/rolled back:" "$REVERT_COUNT"
printf "  %-35s %s\n" "Accepted changes:" "$ACCEPTED"
printf "  %-35s %s%%\n" "Rework rate:" "$REWORK_RATE"
printf "  %-35s %s hours\n" "Median cycle time:" "$MEDIAN_HOURS"
printf "  %-35s %s lines\n" "Average PR size:" "$AVG_SIZE"
echo ""
echo "  Missing (requires manual input):"
echo "    - Reviewer-minutes per accepted change"
echo "    - Defect escape rate"
echo "    - Cost per accepted change (use cost-calculator.py)"
echo ""

# ── CSV output ────────────────────────────────────────
CSV_FILE="delivery-metrics.csv"
if [[ ! -f "$CSV_FILE" ]]; then
    echo "date,weeks_back,merged_prs,reverts,accepted_changes,rework_rate_pct,median_cycle_hours,avg_pr_size" > "$CSV_FILE"
fi
echo "$(date +%Y-%m-%d),$WEEKS,$MERGED_COUNT,$REVERT_COUNT,$ACCEPTED,$REWORK_RATE,$MEDIAN_HOURS,$AVG_SIZE" >> "$CSV_FILE"
echo "  Appended to $CSV_FILE"
