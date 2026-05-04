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

- **Visible** (`tests/visible/`, 9 tests across 4 files): basic happy paths.
- **Held-out** (`tests/holdout/`, 25 tests): edge cases, error paths, and
  performance/efficiency probes (e.g. `fib(100)` will time out under naive
  recursion). Copied into the workdir only after the agent finishes.

## What we're watching

The headline question: **do either of these plugins actually dispatch
subagents when handed a literally embarrassingly-parallel task?**

`Task` / `Agent` tool-call counts and sidechain entry counts in the
analyzer table will answer it directly. Everything else is the standard
cost / correctness panel from the previous experiments.

## Run

```sh
cd experiments/parallelism-comparison
uv run python run.py --reps 5
uv run python analyze.py
```
