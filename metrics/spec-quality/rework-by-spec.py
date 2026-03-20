#!/usr/bin/env python3
"""
Rework rate by spec status — compares rework rates for spec'd vs unspec'd changes.

Chains the spec coverage scanner with the rework detector to answer:
"Do changes with specs produce less rework than changes without specs?"

Usage:
    # Generate both inputs first:
    python spec-coverage.py --repo owner/repo --json spec.json
    python rework-detector.py --repo owner/repo --json rework.json

    # Then compare:
    python rework-by-spec.py --spec spec.json --rework rework.json
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Rework rate by spec status")
    parser.add_argument("--spec", required=True, help="JSON from spec-coverage.py")
    parser.add_argument("--rework", required=True, help="JSON from rework-detector.py")
    args = parser.parse_args()

    with open(args.spec) as f:
        spec_data = json.load(f)
    with open(args.rework) as f:
        rework_data = json.load(f)

    # Build lookup: PR number or SHA -> has_spec
    spec_by_number = {}
    for pr in spec_data.get("prs", []):
        spec_by_number[pr["number"]] = pr["has_spec"]

    # Build lookup: SHA -> rework status
    # Try to match by PR number if available, otherwise by SHA prefix
    rework_by_sha = {}
    for item in rework_data:
        rework_by_sha[item["sha"]] = item

    # Match: for each rework item, check if we have spec data
    specd_total = 0
    specd_rework = 0
    unspecd_total = 0
    unspecd_rework = 0
    unmatched = 0

    for item in rework_data:
        if item["status"] == "pending":
            continue

        # Try to match by PR number
        pr_num = item.get("pr_number")
        if pr_num and pr_num in spec_by_number:
            has_spec = spec_by_number[pr_num]
        else:
            # Can't match — count as unmatched
            unmatched += 1
            continue

        if has_spec:
            specd_total += 1
            if item["status"] == "rework":
                specd_rework += 1
        else:
            unspecd_total += 1
            if item["status"] == "rework":
                unspecd_rework += 1

    specd_rate = (specd_rework / specd_total * 100) if specd_total > 0 else 0
    unspecd_rate = (unspecd_rework / unspecd_total * 100) if unspecd_total > 0 else 0

    print()
    print("=" * 50)
    print(" REWORK RATE BY SPEC STATUS")
    print("=" * 50)
    print()
    print(f"  With spec:     {specd_rework}/{specd_total} reworked = {specd_rate:.1f}%")
    print(f"  Without spec:  {unspecd_rework}/{unspecd_total} reworked = {unspecd_rate:.1f}%")
    print()

    if unmatched > 0:
        print(f"  ({unmatched} changes could not be matched between datasets)")
        print()

    if specd_total > 0 and unspecd_total > 0:
        if unspecd_rate > specd_rate:
            diff = unspecd_rate - specd_rate
            print(f"  Unspec'd changes have {diff:.1f} percentage points more rework.")
            print(f"  Specs are working.")
        elif specd_rate > unspecd_rate:
            diff = specd_rate - unspecd_rate
            print(f"  Spec'd changes have {diff:.1f} percentage points MORE rework.")
            print(f"  Specs may not be effective — check spec quality.")
        else:
            print(f"  No difference. Specs may be performative.")
    print()


if __name__ == "__main__":
    main()
