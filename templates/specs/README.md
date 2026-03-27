# Spec Process Guide

## The process

Specs have two parts that serve two different purposes and are filled out at different times.

### Step 1: Define intent (human side)

Before any implementation starts, answer the five forcing-function questions. These are for humans — a leader should be able to audit them in 60 seconds.

Do this first. Get it reviewed. If the intent is unclear, no amount of technical precision downstream will save you. You are not ready to build until all five questions have substantive answers.

Use the `/intent-check` Claude Code command for an interactive version that pushes back on vague answers.

### Step 2: Fill the constraint surface (machine side)

Once intent is approved, translate it into machine-readable constraints: model anchors (specific files the AI should read), scope boundaries (specific modules it must not touch), acceptance criteria (deterministic checks), and blind spots to watch for.

This is what the AI consumes. The more precise it is, the less the AI invents.

### Step 3: Break into mini-plans

For any change expected to exceed ~400 lines, break the work into phases before implementation begins. Each phase should be:

- **Small enough to review** (~400 lines or less per phase)
- **Independently verifiable** (has its own success criteria, both automated and manual)
- **Independently committable** (the codebase is in a good state after each phase)

Write the mini-plan as a checklist of phases. For each phase, name:
1. What changes (which files, what behavior)
2. Automated verification (commands that prove it works)
3. Manual verification (what a human checks before proceeding)

A human reviews the mini-plan before any phase executes. This is where review has the highest leverage — a bad line in a plan cascades into hundreds of bad lines of code.

### Step 4: Implement phase by phase

Execute one phase at a time. Run automated verification after each phase. Pause for manual verification before proceeding to the next. If something doesn't match the plan, stop and reassess rather than improvising.

## Templates

### [swe/](swe/) — Software Engineering

The **Delivery Spec Template** for implementation tasks. Two halves:
- **Intent** (human side): five forcing-function questions, rollback plan, ownership
- **Constraint surface** (machine side): model anchors, scope boundaries, constraints, style rules, acceptance criteria, blind spots

### [ml-research/](ml-research/) — ML Research

The **ML Research Spec** for experiments, model training, and research tasks. Three required sections (research direction, success metric, constraints) plus optional sections. The spec defines what success looks like and what you cannot do, not the approach.

## Improvement Prompts

Each discipline includes a companion **improvement prompts** file with per-section questions to help you fill gaps:

- **[improvement-prompts.md](improvement-prompts.md)** — General prompts (ambiguity, testability, consistency, completeness)
- **[swe/02-improvement-prompts.md](swe/02-improvement-prompts.md)** — Section-by-section prompts for the SWE spec
- **[ml-research/02-improvement-prompts.md](ml-research/02-improvement-prompts.md)** — Section-by-section prompts for the ML Research spec

## Design Principles

1. **Human sections provide direction, machine sections provide precision.** Humans define *what* and *why*. Machines execute *how*.

2. **Machine sections are placed last.** LLMs exhibit recency bias. Putting executable sections at the end means the AI is most attentive to the rules it must follow.

3. **Review the plan, not the code.** Reviewing 200 lines of a mini-plan catches more problems than reviewing 2,000 lines of generated code. Errors in intent and planning cascade; errors in code are local.
