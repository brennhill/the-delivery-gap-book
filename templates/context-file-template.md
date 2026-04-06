# CLAUDE.md Template

Keep this file under 200 lines. If it grows past that, move detail into `.claude/rules/` files with `paths:` frontmatter for scoped loading.

**Litmus test for every line:** Would removing this cause the AI to make mistakes? If not, cut it.

---

```markdown
# CLAUDE.md

## Project
[One sentence: what this project does and who it's for.]

## Commands
[Only commands the AI cannot guess. Skip standard ones like `npm install`.]

```bash
make check          # lint + test + format check
make build          # build binary + frontend
npm test -- --run   # run frontend tests (no watch mode)
```

## Architecture
[How the code is organized. Which layers exist. What calls what.]

- Strict layering: handler -> service -> storage. No layer skipping.
- Frontend: React + TypeScript in `web/`. Backend: Go with Chi router.
- See `docs/ARCHITECTURE.md` for full details.

## Conventions
[Rules that differ from language defaults. Skip anything the AI would do naturally.]

- Nullable DB columns use pointer types (*string, *int64)
- All JSON endpoints use `http.MaxBytesReader` to cap request body size
- Error responses follow `{"error": "message"}` shape consistently

## Do Not
[Hard rules. Things the AI must never do in this codebase.]

- Do not skip pre-commit hooks
- Do not modify migration files after they've been applied
- Do not add dependencies without checking for existing alternatives first
```

---

## Scaling with `.claude/rules/`

When your root CLAUDE.md approaches 200 lines, split into scoped rules:

```markdown
<!-- .claude/rules/api-conventions.md -->
---
paths:
  - "src/api/**/*.ts"
  - "src/routes/**/*.ts"
---

API endpoints follow REST conventions. Always validate input with Zod schemas.
Error responses use RFC 7807 Problem Details format.
Rate limiting is handled by middleware — do not add per-route limits.
```

Rules with `paths:` frontmatter only load when the AI touches matching files. Rules without `paths:` load unconditionally.

## Cross-tool compatibility

For teams using multiple AI tools (Cursor, Claude Code, Codex):

```markdown
<!-- CLAUDE.md -->
@AGENTS.md

<!-- AGENTS.md contains shared rules -->
<!-- .cursorrules or .cursor/rules/ for Cursor-specific rules -->
```

Stripe syncs rules across Minions, Cursor, and Claude Code. Keep shared rules in one file and import from tool-specific configs.

## What does NOT belong

- Anything the AI can infer by reading code
- Standard language conventions it already knows
- Detailed API documentation (link to it instead)
- Information that changes frequently
- File-by-file codebase descriptions
- Self-evident practices ("write clean code", "follow best practices")

## Anti-patterns

| Pattern | Why it fails |
|---------|-------------|
| 500+ line CLAUDE.md | Important rules get lost in noise; AI ignores them |
| "Format code properly" | Too vague — "Use 2-space indentation" is enforceable |
| Contradictory rules across files | Causes arbitrary behavior |
| Never pruning | Stale rules accumulate; treat like code — review and delete |
| Duplicating what code says | Wastes context tokens on things the AI discovers by reading files |
