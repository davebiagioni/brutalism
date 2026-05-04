# TDD plugin comparison

A reproducible experiment that asks two different "implementation philosophies"
to make the same fixed test suite pass, then compares cost and code shape.

- **Toy task**: implement an LRU cache (`task.md`, `tests/test_lru.py`)
- **Arms**:
  - `brutalism` — invokes the brutalism skill from this repo
  - `superpowers` — invokes the test-driven-development skill from the
    `superpowers` plugin
- **Same prompt scaffold for both**, only the closing instruction differs
  (`prompts/brutalism.md` vs `prompts/superpowers.md`).

## What gets measured

The harness runs each arm headlessly via `claude -p --session-id ...` and reads
the resulting JSONL transcript from `~/.claude/projects/<sanitized-cwd>/`.

Per arm, per repetition:

- wall time (subprocess and from transcript timestamps)
- assistant turns
- input / output / cache-creation / cache-read tokens
- total tool calls and per-tool breakdown
- subagent invocations (`Task` / `Agent` tool calls) and sidechain entries
- final implementation size (lines, non-blank lines, chars)
- whether the fixed test suite passes

## Requirements

- `claude` on `PATH` (already authenticated)
- `uv` on `PATH` (used to spawn an ephemeral pytest env per run)
- Both plugins available in the user's Claude Code env:
  - `brutalism` → this repo, presumed on `--plugin-dir` or installed
  - `superpowers` → installed under `~/.claude/plugins/`

## Run

```sh
cd experiments/tdd-comparison

# vibe check: one rep per arm
uv run python run.py

# tighter numbers: 3 reps per arm
uv run python run.py --reps 3

# only one arm, with a specific model
uv run python run.py --arms brutalism --model sonnet

uv run python analyze.py
```

`run.py` writes per-run metadata to `results/runs.json` and leaves each arm's
working tree under `results/<arm>-NN/` so you can inspect the generated code.
`analyze.py` prints the comparison table and writes `results/summary.json`.

`results/` is gitignored; commit selectively if you want to share findings.

## Caveats

- **Real money**: each run is a real `claude -p` invocation. A single arm pair
  with default settings is small (the task is small), but `--reps 5` adds up.
- **Variance**: model sampling alone can swing token counts 2-3x. Use `--reps`
  for any claim stronger than "vibe check".
- **Environment leak**: the harness uses your user-level `claude` setup, so
  hooks, CLAUDE.md, and other installed plugins are active for both arms. The
  only deliberate difference is the closing line of the prompt.
- **Per-tool-call billing**: token counts include cache reads at full input
  rate; consult Anthropic pricing if converting to dollars.
