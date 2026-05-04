# Correctness comparison: brutalism vs. superpowers

The follow-up to `tdd-comparison/`. Same harness skeleton, but the visible
tests deliberately under-specify the task — the agent is graded against a
larger held-out suite it never sees.

## Task

Arithmetic expression evaluator (`task.md`):

- `+ - * / % **` plus parens and unary `-`
- `**` is right-associative; binds tighter than unary `-` (so `-2**2 == -4`)
- `/` always returns a float; `*` between ints stays int
- Errors map to `ValueError` / `ZeroDivisionError`

## Test split

- **Visible** (`tests/visible/`, 6 tests): basic precedence and one example
  of each operator. Copied into the workdir so the agent can run pytest.
- **Held-out** (`tests/holdout/`, 22 tests): edge cases — right-associativity
  of `**`, unary-minus chains, error paths, whitespace, etc. Copied into the
  workdir **after** the agent finishes, used only for grading.

## Run

```sh
cd experiments/correctness-comparison
uv run python run.py             # 1 rep per arm
uv run python run.py --reps 5    # tighter numbers
uv run python analyze.py
```

The analyzer adds `visible pass rate` and `HOLDOUT pass rate` rows to the
table from experiment 1, plus a per-test failure histogram so you can see
which edges each arm tends to drop.

## Caveats

- **Permission scope**: the agent runs with `--permission-mode
  bypassPermissions`, so a curious agent could in principle walk up the
  directory tree and find the held-out tests. The prompt scopes the task to
  the visible tests only; both arms have, in practice, stayed in the
  workdir. If this experiment is repeated against a more exploratory agent,
  move the held-out file to a path outside the experiment tree.
- **Spec authority**: the task spec in `task.md` is more detailed than the
  visible tests on purpose. The held-out tests cover behaviors the spec
  guarantees but the visible tests don't probe. An arm that reads the spec
  carefully should generalize; one that just makes the visible tests green
  will leak failures.
