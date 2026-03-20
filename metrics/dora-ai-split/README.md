# DORA Metrics — AI vs Non-AI Split

The question the book asks: "Is AI helping delivery, or just making activity charts look better?"

You can't answer that without splitting your DORA metrics by AI-assisted vs human-only changes. This guide shows how to set it up end-to-end, including MTTR via Jira.

---

## The Four DORA Metrics, Split

| Metric | What it answers | AI-specific question |
|--------|----------------|---------------------|
| **Deployment frequency** | How often do you ship? | Are AI-assisted changes shipping faster or piling up in review? |
| **Lead time for changes** | How long from commit to production? | Do AI PRs merge faster, or sit longer in review? |
| **Change fail rate** | How often do deploys break things? | Do AI-assisted deploys fail more often? |
| **Recovery time (MTTR)** | How fast do you recover from failure? | Are AI-related incidents harder to diagnose and fix? |

---

## Step 1: Identify AI-Assisted Changes

Before you can split, you need to tag which changes are AI-assisted. Pick one or more of these detection methods:

### Option A: Co-authored-by trailers (automatic)

Most AI coding tools add a trailer to the commit message:

```
Co-Authored-By: Claude <noreply@anthropic.com>
Co-authored-by: Copilot <noreply@github.com>
```

Detect with:
```bash
git log --since="4 weeks ago" --grep="Co-[Aa]uthored-[Bb]y.*anthropic\|copilot\|cursor\|openai\|devin" --oneline | wc -l
```

### Option B: PR labels (team convention)

Add a required label to your PR template: `ai-assisted` or `human-only`. Enforce in CI:

```yaml
# GitHub Actions: require ai label
- name: Check AI label
  run: |
    LABELS=$(gh pr view ${{ github.event.pull_request.number }} --json labels --jq '.labels[].name')
    if ! echo "$LABELS" | grep -qE "ai-assisted|human-only"; then
      echo "::error::PR must have 'ai-assisted' or 'human-only' label"
      exit 1
    fi
```

### Option C: Branch naming convention

Convention: `ai/feature-name` for AI-assisted, normal naming for human.

### Option D: Commit message prefix

Convention: `[ai]` prefix on AI-assisted commit messages.

**Recommendation:** Option A is automatic and retroactive. Option B is most reliable going forward. Use both.

---

## Step 2: Deployment Frequency & Lead Time (from git)

Once you can identify AI vs non-AI changes, split the delivery-baseline metrics:

```bash
# AI-assisted PRs merged to main in last 4 weeks
AI_COUNT=$(git log --merges --since="4 weeks ago" --grep="Co-[Aa]uthored-[Bb]y.*anthropic\|copilot\|cursor" --oneline | wc -l)

# All PRs merged to main
TOTAL_COUNT=$(git log --merges --since="4 weeks ago" --oneline | wc -l)

# Human-only
HUMAN_COUNT=$((TOTAL_COUNT - AI_COUNT))

echo "AI-assisted: $AI_COUNT"
echo "Human-only: $HUMAN_COUNT"
echo "AI share: $(echo "scale=1; $AI_COUNT * 100 / $TOTAL_COUNT" | bc)%"
```

For lead time, use the `reviewer-minutes.py` script and split by label or trailer.

---

## Step 3: Change Fail Rate (from git + Jira)

### Which deploys failed?

A "failed deployment" is one that caused an incident, rollback, or hotfix. You need to link deploys to incidents.

**In Jira:**

1. Create a custom field on your incident tickets: `Triggered By Change` (link to the PR or commit SHA)
2. Label incidents: `ai-related` if the triggering change was AI-assisted
3. Query:

```
project = OPS AND type = Incident AND created >= -4w
```

Split by the `ai-related` label:

```
# AI-related incidents
project = OPS AND type = Incident AND created >= -4w AND labels = ai-related

# Non-AI incidents
project = OPS AND type = Incident AND created >= -4w AND labels != ai-related
```

**Change fail rate:**

```
AI change fail rate    = AI incidents / AI deploys
Human change fail rate = human incidents / human deploys
```

If you don't have this Jira setup yet, start tagging this week. You need 4 weeks of data before the split becomes meaningful.

---

## Step 4: Recovery Time / MTTR (from Jira)

MTTR = time from incident creation to resolution. This is the metric that's hardest to get from git alone — you need your incident tracker.

### Jira setup

**Required fields on incident tickets:**
- `Created` (automatic)
- `Resolved` (automatic when moved to Done)
- `Triggered By Change` (custom field — PR number or commit SHA)
- Labels: `ai-related` or left blank

**JQL for MTTR:**

```
# All incidents, last 4 weeks
project = OPS AND type = Incident AND created >= -4w AND resolved IS NOT EMPTY
```

**Computing MTTR:**

Export from Jira (CSV or API) and compute:

```python
import csv
from datetime import datetime

incidents = []
with open("jira_export.csv") as f:
    for row in csv.DictReader(f):
        created = datetime.strptime(row["Created"], "%Y-%m-%dT%H:%M:%S.%f%z")
        resolved = datetime.strptime(row["Resolved"], "%Y-%m-%dT%H:%M:%S.%f%z")
        mttr_hours = (resolved - created).total_seconds() / 3600
        is_ai = "ai-related" in row.get("Labels", "")
        incidents.append({"mttr_hours": mttr_hours, "ai": is_ai})

ai_incidents = [i for i in incidents if i["ai"]]
human_incidents = [i for i in incidents if not i["ai"]]

if ai_incidents:
    ai_mttr = sum(i["mttr_hours"] for i in ai_incidents) / len(ai_incidents)
    print(f"AI MTTR:    {ai_mttr:.1f} hours ({len(ai_incidents)} incidents)")

if human_incidents:
    human_mttr = sum(i["mttr_hours"] for i in human_incidents) / len(human_incidents)
    print(f"Human MTTR: {human_mttr:.1f} hours ({len(human_incidents)} incidents)")
```

### Jira API alternative

```bash
# Fetch incidents via Jira REST API
curl -u user@company.com:$JIRA_TOKEN \
  "https://yourcompany.atlassian.net/rest/api/3/search" \
  -G --data-urlencode 'jql=project = OPS AND type = Incident AND created >= -4w' \
  --data-urlencode 'fields=created,resolutiondate,labels' \
  -H "Accept: application/json" > incidents.json
```

### Linear alternative

Linear exposes similar data via GraphQL:

```graphql
{
  issues(filter: {
    team: { key: { eq: "OPS" } }
    labels: { name: { eq: "incident" } }
    createdAt: { gte: "2026-02-20" }
  }) {
    nodes {
      identifier
      title
      createdAt
      completedAt
      labels { nodes { name } }
    }
  }
}
```

Split by label the same way.

---

## Step 5: The Dashboard

Once you have all four metrics split, the weekly scorecard becomes:

| Metric | AI-assisted | Human-only | Delta |
|--------|------------|-----------|-------|
| Deployment frequency | X/week | Y/week | |
| Lead time (median) | X hours | Y hours | |
| Change fail rate | X% | Y% | |
| MTTR | X hours | Y hours | |

**What to look for:**

- AI lead time *higher* than human? → Review bottleneck. AI PRs are sitting in the queue.
- AI change fail rate *higher*? → Gate coverage insufficient for AI-generated code. Add tiers.
- AI MTTR *higher*? → AI-generated code is harder to debug. Check trace infrastructure.
- AI deployment frequency *lower* despite more PRs? → Productivity trap. Volume up, delivery flat.

---

## What This Does NOT Do

This setup requires manual tagging (labels, co-authored-by conventions) and Jira/Linear configuration. There is no fully automated way to detect all AI-assisted changes retroactively, and no way to get MTTR without an incident tracker.

The honest starting point: tag changes going forward, start measuring in 4 weeks, and use the split to answer "is AI helping delivery?" with data instead of intuition.

---

## Further Reading

- [DORA: Software delivery performance metrics](https://dora.dev/guides/dora-metrics/)
- [DORA: A history of software delivery metrics](https://dora.dev/guides/a-history-of-doras-software-delivery-metrics/)
- [Faros AI: AI Productivity Paradox](https://www.faros.ai/ai-productivity-paradox) — PR volume +98%, net throughput zero
- [DX: AI-Assisted Engineering Q4 2025](https://getdx.com/report/ai-assisted-engineering-q4-impact-report/) — Only 22% of merged code is actually AI-authored
