# DS Project Challenge Template

> For leaders reviewing data science projects. Best filled out interactively using the `/challenge-ds` command, which walks through each section in plain language.
>
> This is not a technical review. It is a decision-support document. The goal is to make sure the person approving this project understands what they are approving.

---

## Project Summary (plain language)

### What is the team trying to do?
*Explain in one paragraph, no jargon. What business question does this answer? Who uses the output? What do they do with it?*

### Does the leader's understanding match the team's?
*If not, that's the first red flag. Clarify before proceeding.*

---

## Assumptions

*Every DS project stands on assumptions. List each one and whether it has been verified.*

| Assumption | Verified? | What happens if wrong |
|-----------|-----------|----------------------|
| Historical data represents future behavior | | |
| Labels in the training data are correct | | |
| Features will be available the same way in production | | |
| The data is representative of the full population | | |
| [add more] | | |

---

## What failure looks like

*DS projects fail more often than they succeed. That's normal. The question is whether you'll know when to stop.*

### If the model doesn't perform well enough:
*What's the fallback? What happens to the business problem?*

### If the model works on test data but not in production:
*How will you know? What's the monitoring plan?*

### If the model works but nobody uses the output:
*Has the consumer been involved? Do they know what they're getting?*

### Kill criteria:
*What result tells the team to stop? At what checkpoint? If there are no kill criteria, this is the most important gap to fill.*

---

## Data Reality Check

### What data actually exists?
*Not what you wish existed — what's queryable today?*

### How clean is it?
*Has anyone looked at the raw data? What's missing, duplicated, or stale?*

### Consequences of data issues:
*Dirty data → the model learns noise, not signal. Missing data → systematic bias. Old data → may not represent the current business. Data cleanup is not a minor task.*

---

## Alternatives Considered

*Has the team considered simpler approaches?*

| Alternative | Why it might work | Why it might not | Estimated effort |
|------------|-------------------|------------------|-----------------|
| Business rules (no model) | | | |
| Simple analysis/report | | | |
| Intervene on entire population | | | |
| [team's proposed approach] | | | |

*No alternative is "easy." Every approach has costs. The point is to compare them honestly.*

---

## Key Tradeoffs

*These are business decisions, not technical ones. The leader should make them.*

### Accuracy vs speed to deploy:
*A simple model in two weeks at 80% accuracy, or a sophisticated one in two months at 90%? Is the extra 10% worth the wait?*

### Precision vs recall:
*Catch every possible case (more false alarms) or only flag high-confidence cases (miss some real ones)? What's the cost of each error type?*

### Complexity vs maintainability:
*Who owns this model after the DS team moves on? Can they debug and retrain it?*

### Automation vs human oversight:
*Should the model make decisions automatically or flag for human review? What's the cost of a wrong automated decision?*

---

## Questions for Status Updates

*Ask these at every check-in:*

1. Are we on track to hit the kill criteria checkpoint?
2. What's model performance on the holdout set? Above the minimum threshold?
3. Have you validated on a time period the model hasn't seen?
4. What's the biggest risk you see right now?
5. Is the consumer of this output involved and ready to use it?

*DS progress doesn't look like engineering progress. No feature checklist. You'll see experiments — some work, some don't. Watch for convergence vs going in circles.*

---

## Risk Summary

| | |
|---|---|
| **Project** | |
| **Business question** | (plain language) |
| **Timeline** | |
| **Confidence level** | (high / medium / low — be honest) |
| **Key risks** | 1. ... 2. ... 3. ... |
| **Unmitigated risks** | (any NOT YET addressed) |
| **Kill criteria** | |
| **First checkpoint** | |
| **Go/no-go recommendation** | (honest read) |
