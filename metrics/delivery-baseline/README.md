# Delivery Baseline Metrics

Computes baseline metrics from git history and the GitHub API without requiring a commercial platform.

## Usage

```bash
chmod +x delivery-metrics.sh

# Local defaults (4 weeks)
./delivery-metrics.sh

# Custom lookback
./delivery-metrics.sh --weeks 8

# GitHub repo
./delivery-metrics.sh --repo owner/repo
```

## What It Measures

- Merged PR count
- Reverted PR count (by title pattern)
- Rework rate (reverts / merged)
- Median PR cycle time (open → merge)
- Average PR size (lines changed)

## What It Does NOT Measure

These require manual input or additional tooling:
- Reviewer-minutes per accepted change
- Defect escape rate
- Cost per accepted change (use the cost calculator)
