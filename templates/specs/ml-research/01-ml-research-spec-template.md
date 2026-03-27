# ML Research Spec

Sections marked 👤 are human-authored context. Sections marked 🤖 are machine-executable.
Optional sections are scored only if included — omitting them does not penalize completeness.

---

## 1) Research Direction 👤 (required)
- Hypothesis:
- What are we trying to learn:
- Why this matters now:

## 2) Success Metric 👤 (required)
- Primary metric: (e.g., `val_bpb < 1.05`, `F1 > 0.92`)
- Threshold for "success":
- Threshold for "stop and rethink":
- Evaluation method: (offline eval / A/B test / human eval)

## 3) Constraints 👤 (required)
- Compute budget: (e.g., single H100, 5-min wall clock)
- Data budget: (e.g., 10B tokens, existing dataset only)
- Time budget:
- Ethical/compliance boundaries:
- What the agent must NOT change:

---

*Optional sections below — include what applies. Each section is scored if present.*

## 4) Data Specification 🤖 (optional)
- Training data source:
- Validation data source:
- Feature engineering:
- Data quality requirements:
- Preprocessing pipeline:

## 5) Techniques 🤖 (optional)
- Model architecture:
- Algorithm choices:
- Hyperparameter ranges:
- Baseline to beat:

## 6) Experimentation Plan 🤖 (optional)
- Offline evaluation protocol:
- A/B test design:
- Statistical significance criteria:
- Iteration strategy: (grid search / Bayesian / agent-autonomous)

## 7) Human-in-the-Loop 👤 (optional)
- When does a human review results:
- Escalation criteria:
- Go/no-go decision process:

## 8) Infrastructure 🤖 (optional)
- Hardware requirements:
- Deployment environment:
- Dependencies and versions:

## 9) Monitoring 🤖 (optional)
- Model drift detection:
- Data quality alerts:
- Performance regression thresholds:
- Logging and observability:

## 10) Cost 👤 (optional)
- Estimated compute cost per experiment:
- Total budget cap:
- Cost-per-improvement tracking:

## 11) Integration Points 🤖 (optional)
- Upstream data dependencies:
- Downstream consumers:
- API contracts:
- Rollback mechanism:
