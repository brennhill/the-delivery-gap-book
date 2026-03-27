# Specs and Process

The spec is a forcing function for thinking. The document is a side effect.

This directory contains everything you need to define features before AI writes code: the process, the commands that walk you through it, and the templates.

## The Process

Four phases, each building on the last. Do not skip ahead.

### Phase 1: Intent — WHY are we doing this?

Five forcing-function questions. Answer them before anything else.

1. **What problem does this solve?** (Not what it builds — what problem goes away?)
2. **How will we know it worked?** (An existing metric that will move, not one invented for the project)
3. **What is out of scope?** (Explicit boundaries the AI must not cross)
4. **What must NOT happen?** (Constraints and negation — the genie's missing instructions)
5. **Pre-mortem findings** (30 minutes: why could this fail?)

The AI pushes back on vague answers. If you can't answer these, you're not ready to build.

### Phase 2: Behavioral Spec — WHAT does the user experience?

A funnel from broad to specific:

1. **Stories** — What does the user do today? What should they experience instead?
2. **Mechanism** — Why will this approach solve the problem? Challenge the causal logic.
3. **States and transitions** — What are all the states? What moves between them?
4. **Error cases** — What happens when things fail? When users do something unexpected?

Each level must be solid before the next. Bad ideas die here, cheaply.

For DS work, this phase becomes **Experimental Design**: hypothesis, evaluation contract, data requirements, failure modes.

### Phase 3: Design Conversation — HOW will we approach this?

The AI researches the codebase (or data, for DS) and presents what exists:
- How similar features work
- What patterns, conventions, and infrastructure are available
- Options with tradeoffs

The user makes design decisions. The AI presents options, not recommendations.

### Phase 4: Implementation Design — WHERE does the code go?

The AI proposes specific architecture and **challenges the codebase itself**:
- If the area has inconsistent patterns, it flags them
- If there are multiple places the code could go, that ambiguity is a risk signal
- Cleanup becomes a prerequisite in the implementation plan, not an afterthought

This is the anti-slop gate.

### Then:

- **`/plan`** — breaks the spec into ~400 LOC implementation phases (cleanup first if flagged)
- **`/build`** — executes phase by phase with strict TDD and human verification between each

## Commands

Install these in your project's `.claude/commands/` directory.

### Feature definition

| Command | What it does |
|---------|-------------|
| [`feature.md`](commands/feature.md) | Four-phase feature definition for software engineering |
| [`feature-ds.md`](commands/feature-ds.md) | Four-phase feature definition for data science |

### Implementation

| Command | What it does |
|---------|-------------|
| [`plan.md`](commands/plan.md) | Break a spec into ~400 LOC implementation phases |
| [`build.md`](commands/build.md) | Execute plan phase by phase with TDD and verification |

### Leadership

| Command | What it does |
|---------|-------------|
| [`challenge-ds.md`](commands/challenge-ds.md) | Walk a leader through a DS project — explains simply, surfaces risks, sets realistic expectations |

### Usage

```bash
# Software engineering:
/feature                         # Intent → behavior → design → implementation
/plan specs/my-feature.md        # Break into phases
/build specs/my-feature-plan.md  # Execute with TDD

# Data science:
/feature-ds                      # Same flow, DS vocabulary

# For leaders reviewing DS projects:
/challenge-ds                    # Or: /challenge-ds specs/my-model.md
```

## Templates

Use these as reference or fill them out manually. The `/feature` and `/feature-ds` commands produce the same output interactively.

| Template | For |
|----------|-----|
| [`templates/swe/01-one-page-spec-template.md`](templates/swe/01-one-page-spec-template.md) | Software engineering features |
| [`templates/ds-spec-template.md`](templates/ds-spec-template.md) | Data science features |
| [`templates/ds-challenge-template.md`](templates/ds-challenge-template.md) | Leader review of DS projects |
| [`templates/ml-research/01-ml-research-spec-template.md`](templates/ml-research/01-ml-research-spec-template.md) | ML research experiments |

### Improvement prompts

Per-section questions to sharpen a draft spec:

| File | Scope |
|------|-------|
| [`templates/improvement-prompts.md`](templates/improvement-prompts.md) | General (ambiguity, testability, consistency) |
| [`templates/swe/02-improvement-prompts.md`](templates/swe/02-improvement-prompts.md) | SWE spec sections |
| [`templates/ml-research/02-improvement-prompts.md`](templates/ml-research/02-improvement-prompts.md) | ML research spec sections |

## Design Principles

1. **Human sections provide direction, machine sections provide precision.** Humans define *what* and *why*. Machines execute *how*.

2. **Each phase is a gate.** Do not proceed until the current phase is solid. Bad intent produces bad specs. Bad specs produce bad code. The leverage is highest at the top.

3. **Review the plan, not the code.** Reviewing 200 lines of a plan catches more problems than reviewing 2,000 lines of generated code. Errors in intent cascade; errors in code are local.

4. **Challenge the codebase, not just the feature.** If the existing code is sloppy, building on top of it makes it worse. Cleanup is a prerequisite, not a nice-to-have.
