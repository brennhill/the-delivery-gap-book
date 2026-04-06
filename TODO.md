# Delivery Gap Toolkit — TODO

## High Priority

- [ ] **Copy-pasteable GitHub Actions workflow** — A single `.github/workflows/delivery-gap-gates.yml` that wires up Tier 0 gates (lint, type check, secret detection, PR size limit) for any language. Every guide says "add this to CI" but no file exists to copy.
- [ ] **Filled-out CLAUDE.md example** — The template exists but a worked example for a realistic project (e.g., Next.js SaaS app, Go microservice) would make it immediately actionable.
- [ ] **Before-and-after case study** — Walkthrough of "Team X installed these gates, here's what metrics looked like before and after." Even a synthetic composite would be powerful.
- [ ] **Brownfield migration guide** — "What to do when you inherit a codebase with zero gates." The toolkit assumes greenfield. A retrofit guide for codebases with thousands of existing lint warnings would hit the real audience.

## Medium Priority

- [ ] **OpenAPI contract test example** — The API schema contract example uses custom Python schemas. A Pact or oasdiff example against an actual OpenAPI spec would be more realistic.
- [ ] **Agent setup guide for Cursor/Windsurf/Codex** — The CLAUDE.md template covers Claude Code. Teams using other tools need equivalent guidance for `.cursorrules`, Codex configuration, etc.
- [ ] **Tier 2 items from gap analysis** — Devbox/sandbox architecture guide, permission scoping tiers, gate health dashboard, scope violation detection, behavioral baseline setup, stale contract detection.
- [ ] **Update README.md** — Links to quick-start/ and some deleted files need to be removed or redirected.

## Done (this session)

- [x] Iteration-first reframing across all templates
- [x] Six-tier gate architecture with company mappings (Stripe, Spotify, Webflow)
- [x] LLM-as-judge implementation guide
- [x] Stop hooks implementation guide
- [x] Iteration budget policy
- [x] Version-controlled prompts guide
- [x] Task structuring for agents guide
- [x] Adoption playbook
- [x] Visual regression gate guide
- [x] CLAUDE.md template
- [x] Case study links (10 companies)
- [x] Dead/stale URL fixes (14 replacements)
- [x] Removed Upfront commands, skills, codex directory
- [x] Removed spec templates (replaced by iterate-first process)
- [x] Hostile review — cut 38 files (duplicates, blank forms, thin indexes, internal artifacts)
