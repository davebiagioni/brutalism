# Parallelism comparison: brutalism vs. superpowers

Third experiment. Same harness shape; the task is now four independent
micro-utilities, each in its own module. They share nothing — perfect
material for parallel subagent dispatch if the agent decides to fan out.

## Task

Four files in one workdir (`task.md`):

- `palindrome.py` — `is_palindrome(s)`
- `fibonacci.py` — iterative `fib(n)`
- `flatten.py` — recursively flatten nested lists
- `roman.py` — integer → Roman numeral, 1..3999

## Test split

- **Visible** (`tests/visible/`, 8 tests across 4 files): basic happy paths.
- **Held-out** (`tests/holdout/`, 26 tests): edge cases, error paths, and
  performance/efficiency probes (e.g. `fib(100)` will time out under naive
  recursion). Copied into the workdir only after the agent finishes.

## What we're watching

`Task` / `Agent` tool-call counts and sidechain entry counts. The original
question was whether either plugin dispatches subagents on a literally
embarrassingly-parallel task. The finding turned out to be sharper than
that: brutalism (with rule 15) does so deterministically; superpowers,
with the same capability available, does not.

## Run

```sh
cd experiments/parallelism-comparison
uv run python run.py --reps 5
uv run python analyze.py
```

## Result

See [`RESULTS.md`](RESULTS.md). Short version: brutalism dispatched 4.0 ± 0
comrades per rep across N=5; superpowers dispatched 1.6 ± 2.2. Both arms
got 26/26 held-out correctness.
