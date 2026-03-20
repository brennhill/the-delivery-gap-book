# Spec Quality Metrics

Tools for measuring whether your specs are actually reducing downstream waste.

## Scripts

- **spec-coverage.py** — Scans PR descriptions for spec links (URLs, ticket IDs, spec fields). Reports what percentage of merged PRs have a valid spec.
- **rework-by-spec.py** — Compares rework rates for spec'd vs unspec'd changes. Chains with the rework detector to answer: "Do specs actually help?"

## Quick Start

```bash
# Measure spec coverage
python spec-coverage.py --repo owner/repo --weeks 4

# Compare rework rates by spec status
python ../rework-detection/rework-detector.py --repo owner/repo --json rework.json
python spec-coverage.py --repo owner/repo --json spec.json
python rework-by-spec.py --spec spec.json --rework rework.json
```

See [spec_best_practices.md](spec_best_practices.md) for guidance on writing effective specs.
