# ML Research Spec Improvement Prompts

Section-by-section prompts for the ML Research Spec. Use alongside `01-ml-research-spec-template.md`.

Required sections are marked (required). Optional sections are only relevant if you chose to include them.

---

## Research Direction (required)

### Common gaps
- Hypothesis is a goal, not a falsifiable claim
- No explanation of why this direction over alternatives
- Missing the "what we're trying to learn" — just states what to build

### Improvement questions
- Is your hypothesis falsifiable? What evidence would disprove it?
- What alternative approaches did you consider? Why this one?
- If the experiment succeeds, what do you learn? If it fails, what do you learn?

### Before/After
- **Weak:** Research direction: make the model better.
- **Strong:** Hypothesis: replacing global attention with sliding-window attention (SSSL pattern) in all but the last layer will match full-attention quality at 40% lower compute. We're testing whether local context is sufficient for mid-layers.

---

## Success Metric (required)

### Common gaps
- Metric named but no threshold defined
- No "stop and rethink" threshold — experiments run forever
- Evaluation method not specified (offline? A/B? human?)

### Improvement questions
- Can you measure success with a single number?
- What is the threshold for "success"? What number means "stop and rethink"?
- How will you evaluate: offline metrics, A/B test, human evaluation, or some combination?
- Is your metric comparable across experiments? (Fixed eval set? Same tokenizer?)

### Before/After
- **Weak:** Primary metric: val_bpb.
- **Strong:** Primary metric: `val_bpb` on FineWeb-Edu held-out set (1M tokens, fixed seed 42). Success threshold: < 1.05. Stop-and-rethink threshold: > 1.15 after 3 runs. Evaluation: offline only — no A/B test for this research phase.

---

## Constraints (required)

### Common gaps
- No compute budget — experiments scale unboundedly
- No time budget — research stretches indefinitely
- Missing "what the agent must NOT change" — agent rewrites infrastructure

### Improvement questions
- What is the compute budget per experiment? (GPU type, wall-clock time)
- What is the total time budget for this research direction?
- What files, functions, or components must the agent NOT modify?
- Are there ethical or compliance boundaries? (Data sources, model capabilities)

### Before/After
- **Weak:** Use a single GPU.
- **Strong:** Compute: single H100, 5-minute wall clock per experiment. Total budget: 50 experiments (4 GPU-hours). Agent must NOT modify `prepare.py` or the tokenizer. Agent must NOT use data sources outside FineWeb-Edu.

---

## Data Specification (optional)

### Common gaps
- Training data source named but not versioned
- No validation data specification — eval is ad hoc
- Data quality requirements implicit

### Improvement questions
- Is your training data versioned? Can you reproduce the exact dataset?
- Is the validation set fixed across experiments? (Same seed, same split?)
- What preprocessing is applied? Is it deterministic?
- Are there data quality filters? What gets excluded and why?

### Before/After
- **Weak:** Training data: FineWeb.
- **Strong:** Training data: FineWeb-Edu v2, first 10B tokens (deterministic slice via `prepare.py` with seed=42). Validation: held-out 1M tokens (fixed, never modified across experiments). Preprocessing: BPE tokenizer with vocab_size=8192, trained once in `prepare.py`.

---

## Techniques (optional)

### Common gaps
- Architecture described but no baseline to compare against
- Hyperparameter ranges not bounded — search space is infinite
- No justification for algorithm choice

### Improvement questions
- What is the baseline model? What is its current score on your success metric?
- What hyperparameters can the agent tune? What are the allowed ranges?
- Why this architecture/algorithm over alternatives?

### Before/After
- **Weak:** Use a transformer model.
- **Strong:** Baseline: GPT with DEPTH=8, standard global attention, val_bpb=1.12. Agent may modify: DEPTH (4-16), WINDOW_PATTERN (any combination of S/L), learning rate (1e-4 to 1e-2). Agent must NOT change: vocab_size, tokenizer, optimizer (Muon+AdamW).

---

## Experimentation Plan (optional)

### Common gaps
- No protocol for comparing experiments
- No statistical significance criteria
- Iteration strategy unclear — random guessing vs systematic search

### Improvement questions
- How do you ensure experiments are comparable? (Fixed time, fixed data, fixed eval?)
- How many runs do you need to confirm a result is real (not noise)?
- What is your iteration strategy: grid search, Bayesian optimization, or agent-autonomous?

### Before/After
- **Weak:** Run experiments and compare results.
- **Strong:** All experiments run for exactly 5 minutes wall clock (ensures comparability regardless of batch size or model size). Each configuration runs 3 times with different seeds — result is the median. Agent uses greedy search: keep best, vary one parameter at a time.

---

## Human-in-the-Loop (optional)

### Common gaps
- No checkpoint for human review — agent runs indefinitely
- No escalation criteria — agent keeps trying when it should stop
- Go/no-go decision process undefined

### Improvement questions
- After how many experiments does a human review results?
- What triggers escalation? (N consecutive failures? Unexpected resource usage?)
- Who makes the go/no-go decision to continue this research direction?

### Before/After
- **Weak:** Review results periodically.
- **Strong:** Human review after every 10 experiments or if val_bpb improves by > 0.05 in a single step (anomaly check). Escalation: 5 consecutive experiments with no improvement triggers a direction review. Go/no-go: researcher reviews trajectory plot and decides whether to continue, pivot, or stop.

---

## Monitoring (optional)

### Common gaps
- No model drift detection
- No alerts for anomalous training runs
- Logging insufficient to reproduce results

### Improvement questions
- How do you detect if model quality is degrading over time?
- What alerts fire if a training run behaves anomalously? (Loss spike, NaN, OOM)
- Can you reproduce any experiment from the logs alone?

### Before/After
- **Weak:** Monitor training runs.
- **Strong:** Log val_bpb every 100 steps. Alert if loss > 10x baseline at any checkpoint (likely NaN or divergence). Store full config, git SHA, and final val_bpb for every experiment in `experiments.jsonl`. Reproducibility: any experiment can be rerun from its logged config.

---

## Infrastructure (optional)

### Common gaps
- Hardware requirements assumed, not stated
- Dependency versions not pinned
- No mention of reproducibility setup

### Improvement questions
- What GPU type and count is required?
- Are all dependencies pinned to specific versions?
- Can someone reproduce your setup from the spec alone?

---

## Cost (optional)

### Common gaps
- No per-experiment cost estimate
- No total budget cap
- No cost tracking across experiments

### Improvement questions
- What is the estimated compute cost per experiment? (GPU-hours at your provider's rate)
- What is the maximum total budget before requiring approval to continue?
- Are you tracking cumulative spend as experiments run?

---

## Integration Points (optional)

### Common gaps
- No upstream data dependency documented
- Downstream consumers of the model not identified
- No API contract for model serving

### Improvement questions
- Where does your training data come from? What if that source changes?
- Who or what will consume the trained model? (API endpoint? Batch pipeline? Another model?)
- What is the serving contract? (Input format, output format, latency SLA)
