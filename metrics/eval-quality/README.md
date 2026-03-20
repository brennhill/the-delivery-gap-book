# Eval Quality Metrics

Tools for measuring whether your gates are catching defects and whether your review process is sustainable.

## Scripts

- **machine-catch-rate.py** — What percentage of defects are caught by automated gates vs human reviewers. Scans CI failures and review comments from GitHub.
- **reviewer-minutes.py** — How long humans spend reviewing each change. Pulls review timestamps from GitHub API.
- **defect-escape-rate.py** — What percentage of bugs reach production vs caught pre-prod. Supports GitHub Issues (with labels) or manual input for Jira/Linear.
- **change-fail-rate.py** — DORA metric: what percentage of deployments cause production failure. Supports GitHub Actions, GitHub Deployments API, or manual input.

## Quick Start

```bash
# Machine catch rate
python machine-catch-rate.py --repo owner/repo

# Reviewer-minutes per accepted change
python reviewer-minutes.py --repo owner/repo

# Defect escape rate (GitHub Issues with labels)
python defect-escape-rate.py --repo owner/repo

# Defect escape rate (manual, for Jira/Linear users)
python defect-escape-rate.py --production-bugs 5 --preprod-bugs 23

# Change fail rate (GitHub Actions)
python change-fail-rate.py --repo owner/repo --workflow deploy.yml

# Change fail rate (manual)
python change-fail-rate.py --total-deploys 120 --failed-deploys 8
```

See [eval_best_practices.md](eval_best_practices.md) for guidance on building effective eval gates.
