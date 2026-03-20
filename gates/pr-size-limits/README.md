# PR Size Limits

The SmartBear/Cisco study (2,500 reviews, 3.2M lines of code) found:
- Defect detection peaks at 200-400 lines
- Detection rates collapse above 400 lines
- PRs over 1,000 lines show 70% lower defect detection
- Review effectiveness drops after 60 minutes regardless of skill

## Recommended Thresholds

- **Soft limit:** 200 lines (ideal for thorough review)
- **Hard limit:** 400 lines (reject and require split)
- **Emergency flag:** 1,000+ lines (70% lower detection — almost certainly rubber-stamped)

## Implementation

Most CI systems can enforce this with a simple check on the diff size. If AI generated the oversized PR, send it back to the AI to split.

### GitHub Actions

```yaml
- name: Check PR size
  run: |
    LINES=$(gh pr diff ${{ github.event.pull_request.number }} | wc -l)
    if [ "$LINES" -gt 400 ]; then
      echo "::error::PR is $LINES lines. Max 400. Please split."
      exit 1
    fi
```

### GitLab CI

```yaml
check-pr-size:
  script:
    - LINES=$(git diff origin/main...HEAD | wc -l)
    - if [ "$LINES" -gt 400 ]; then echo "PR too large ($LINES lines). Split it."; exit 1; fi
```

