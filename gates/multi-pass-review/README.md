# code-reviewers

Multi-pass AI code review with three specialized perspectives. Based on the CodeX-Verify research (arXiv 2511.16708) showing that diverse review perspectives improve accuracy from 32.8% to 72.4%.

## Claude Code Skill (Recommended)

If you use Claude Code, skip the install — use the `/review` skill instead:

```
/review              # review current diff
/review src/auth.ts  # review a specific file
```

Three passes run in series (correctness → performance → security). Each pass sees prior findings and skips already-flagged issues. No API key, no install, no configuration.

To add the skill to your project, copy `.claude/skills/review/` from this repo.

## Python Library (CI/CD)

For automated pipelines (GitHub Actions, GitLab CI), use the Python package:

```bash
# With Anthropic (default)
pip install -e ".[anthropic]"

# With OpenAI
pip install -e ".[openai]"

# With LiteLLM (100+ providers, cost tracking)
pip install -e ".[litellm]"

# All providers
pip install -e ".[all]"
```

### API Keys

Each provider reads credentials from standard environment variables — no configuration files needed:

| Provider | Environment Variable | Custom URL |
|----------|---------------------|------------|
| Anthropic | `ANTHROPIC_API_KEY` | `ANTHROPIC_BASE_URL` |
| OpenAI | `OPENAI_API_KEY` | `OPENAI_BASE_URL` |
| LiteLLM | Reads the key for whichever provider the model string routes to | Automatic per provider |

LiteLLM routes by model prefix: `anthropic/claude-sonnet-4-5-20250514` reads `ANTHROPIC_API_KEY`, `azure/gpt-4o` reads Azure credentials, `ollama/llama3` routes to local Ollama.

## Usage

```bash
# Review a diff file (sequential — one perspective at a time)
code-reviewers --diff changes.diff

# Review a GitHub PR (parallel — all three at once, faster)
code-reviewers --pr 123 --repo owner/repo --parallel

# Pipe a diff from stdin
git diff main | code-reviewers --parallel

# Pick specific perspectives
code-reviewers --diff changes.diff --perspectives correctness security

# Use a different provider/model
code-reviewers --diff changes.diff --provider litellm --model anthropic/claude-sonnet-4-5-20250514
```

## Perspectives

| Perspective | Focus | Failure class |
|-------------|-------|---------------|
| `correctness` | Logic errors, boundary conditions, null handling, edge cases, missing error handling, broken invariants | Output trust breaks |
| `security` | SQL injection, XSS, hardcoded credentials, path traversal, auth gaps, scope violations | Scope breaks |
| `performance` | N+1 queries, resource leaks, complexity, duplication, dead code | Gates fail / cost invisible |

### Why these perspectives

Research shows AI-generated code has specific, quantifiable failure patterns that justify dedicated review focus:

- **Correctness**: AI code fails on boundary conditions and edge cases at ~3x the human rate (LiveCodeBench). Missing null checks, guard clauses, and error handling are the most common correctness failures.
- **Security**: ~40% of AI-generated code contains exploitable vulnerabilities (NYU Tandon, 2021). Developers using AI assistants rate their code as *more* secure when it is measurably less so (Perry et al., Stanford, 2023).
- **Performance**: AI-generated code duplicates at 8x the rate of human code (GitClear, 2025), choosing copy-paste over refactoring.

## Sequential vs Parallel

- **Sequential** (default): One perspective at a time. Easier to follow output. Good for interactive use.
- **Parallel** (`--parallel`): All perspectives run concurrently via threads. Same cost, ~3x faster. Good for CI/CD.

## As a Library

```python
from delivery_gap_review.reviewer import run_review, format_markdown

results = run_review(
    diff=my_diff_string,
    provider="anthropic",
    model="claude-sonnet-4-5-20250514",
    parallel=True,
    perspectives=["correctness", "security"],
)

report = format_markdown(results, model="claude-sonnet-4-5-20250514", diff_len=len(my_diff_string))
```

## Further Reading

- [Anthropic: Claude Code best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
