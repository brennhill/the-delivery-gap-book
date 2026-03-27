# DS Spec Template

> See [the process guide](../README.md) for how and when to fill this out.
> Best filled out interactively using the `/feature-ds` command, which walks you through each section with pushback and data investigation.

Four sections, each building on the last. Do not skip ahead.

---

## Intent

*WHY are we doing this? Answer before anything else. The `/feature-ds` command will challenge vague answers.*

### 1. What business question does this answer?
*Not what model to build — what decision does this enable? Who makes that decision?*

### 2. How will we know it worked?
*An existing business metric that will move, not a model metric. Not AUC — what business outcome changes?*

### 3. What is out of scope?
*What adjacent problems will this NOT solve? What data will this NOT use?*

### 4. What must NOT happen?
*Constraints: fairness requirements, data restrictions (PII, legal), decisions that must not be automated without human review.*

### 5. Pre-mortem findings
*Why could this fail? Data not representative? Distribution shift? Survivorship bias? Stakeholders won't act on the output?*

### Kill criteria
*What result tells you to stop? At what point do you abandon this approach?*

---

## Experimental Design

*WHAT are we testing? Work through this interactively — hypothesis first, then evaluation, then data, then failure modes.*

### Hypothesis
*State it explicitly. What do you believe is true? What's the null hypothesis?*

### Evaluation Contract
*How will you measure success? What metric, on what data, at what threshold? Distinguish offline (test set) from online (business impact).*

### Data Requirements
*Unit of observation, label, time window, assumptions about the data.*

### Failure Modes
*Cost of each error type (false positive vs false negative). Subpopulations at risk. Edge cases. What happens when the model is confident but wrong?*

---

## Data and Infrastructure

*WHAT data exists and HOW will we approach this? The `/feature-ds` command investigates the data and presents options.*

### Data availability
*What exists, quality, gaps, volume.*

### Existing work
*Prior attempts, reusable models/features/pipelines.*

### Chosen approach
*Approach and rationale. Alternatives considered.*

---

## Implementation Design

*HOW specifically — where does this live? The `/feature-ds` command researches infrastructure and challenges it.*

### Architecture
*Training pipeline, serving (batch/real-time), monitoring, retraining triggers.*

### Structural issues flagged
*Infrastructure slop, inconsistent pipelines, cleanup needed as prerequisites.*

### Constraints
- Fairness/bias:
- Latency:
- Data restrictions:

### Pressure-test results
*DS-specific risks. Check each item or mark N/A.*
- [ ] **Data leakage**: is any feature derived from the label or from future data?
- [ ] **Training/serving skew**: will features be computed the same way in production?
- [ ] **Reproducibility**: can someone else retrain this and get the same result?
- [ ] **Monitoring gaps**: how will you know when the model stops working?
- [ ] **Dependency risk**: what breaks if an upstream data source changes schema or stops updating?

### Rollback Plan
- Trigger signal:
- Method: (previous model version / fallback logic / kill switch)
- Owner:

### Ownership
- DRI:
- Reviewers:
- Decision date:
