# Cost per Accepted Change

No commercial tool computes this metric today. This script does.

## Usage

```bash
# Interactive mode
python cost-calculator.py

# From JSON input
python cost-calculator.py --json costs.json

# With real rework data from git
python rework-detector.py --json rework.json
python cost-calculator.py --json costs.json --from-rework rework.json

# Generate branded HTML report
python cost-calculator.py --json costs.json --from-rework rework.json --html report.html
```

## Input

```json
{
    "model_cost": 4200,
    "infra_cost": 1800,
    "prompting_hours": 30,
    "review_hours": 40,
    "rework_hours": 20,
    "burdened_rate": 120,
    "merged_prs": 88,
    "reverted_prs": 12
}
```

When using `--from-rework`, `merged_prs` and `reverted_prs` are overridden with real data from the rework detector.

## HTML Report

The `--html` flag generates a branded Delivery Gap report with:
- SVG pie chart showing cost breakdown
- Metric cards (cost per change, accepted, merged, reverted)
- Breakdown table with color-coded categories
- Warning cards for rework rate, oversized PRs, and reworked changes
- Commit SHAs linked to GitHub
