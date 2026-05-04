# Results: brutalism vs. superpowers under a held-out test suite

**Setup.** Implement an arithmetic expression evaluator (`task.md`) — operators
`+ - * / % **` with precedence and right-associative `**`. Each arm sees only
6 visible tests; the harness grades against 22 held-out tests after the agent
finishes. N = 5 reps per arm, default model.

## Numbers (mean ± stdev, N=5)

| metric                | brutalism            | superpowers           | ratio   |
|-----------------------|---------------------:|----------------------:|--------:|
| visible passed        |              6  / 6  |               6  / 6  | —       |
| **held-out passed**   |       **20.4 / 22**  |       **21.0 / 22**   | +1 test |
| held-out pass rate    |          0.927       |           0.955       | +2.8 pp |
| wall time (s)         |         34.8 ± 2.9   |         122.8 ± 28.0  | **3.5×** |
| assistant turns       |          9.2 ± 0.4   |          18.8 ± 1.6   | 2.0×    |
| output tokens         |        4,702 ± 1,116 |        30,095 ± 9,377 | **6.4×** |
| total input tokens    |      275,736 ± 13k   |       651,295 ± 79k   | 2.4×    |
| tool calls            |          6  ± 0.0    |           9.6 ± 0.5   | 1.6×    |
| `Task` / subagents    |          0           |           0           | —       |
| **impl lines**        |        **25 ± 2**    |        **134 ± 12**   | **5.3×** |
| impl chars            |          811 ± 96    |        3,970 ± 372    | 4.9×    |

## Held-out tests most often missed

- **brutalism**: `test_whitespace_ignored` (5/5 fails), `test_leading_plus_ok` (3/5 fails)
- **superpowers**: `test_leading_plus_ok` (5/5 fails)

## Read

1. **Superpowers wins on correctness, but barely.** +1 test out of 22 (2.8
   percentage points). Critically, superpowers' lead is *perfectly
   consistent* (stdev 0) — every rep got the exact same 21/22.
2. **Both arms share one blind spot: unary `+`.** Neither
   "brainstorm edge cases" nor "be brutal" caught that `evaluate("+5")` should
   work. The spec doesn't mention it; the visible tests don't probe it.
   Inferring the rule from the operator table required a leap that neither
   arm made reliably. (Brutalism caught it 2/5; superpowers 0/5.)
3. **Brutalism's correctness loss is architectural.** Every rep reached for
   `ast.parse(s, mode="eval")` to delegate parsing to Python — clever, 25
   lines. But `ast.parse(" 1 + 2 ", mode="eval")` raises `IndentationError`
   in Python 3.11. The shortcut inherits a quirk of the host parser. A
   one-line `s = s.strip()` would close the gap.
4. **Superpowers paid 6.4× the output tokens for a hand-rolled lexer +
   recursive-descent parser** (134 lines vs 25). The full parser sidesteps
   the whitespace pothole because tokenization handles whitespace explicitly.
5. **Still zero subagent invocations** in either arm, across 10 runs total.
   Superpowers' `Task` tool stays unused even when the prompt explicitly
   permits `dispatching-parallel-agents`. The model evidently judges this
   task as too small to fan out.

## Cost vs. quality

| arm         | held-out | output tokens | cost per extra correct test |
|-------------|---------:|--------------:|----------------------------:|
| brutalism   |    20.4  |         4,702 | —                           |
| superpowers |    21.0  |        30,095 | ~25,393 tokens              |

Buying that one extra held-out test costs ~25k extra output tokens. Whether
that's a good trade depends on whether the missed edge ships, who finds it,
and how expensive the fix is.

## What this experiment does NOT show

- **Tasks where parallelism matters.** Neither arm dispatched subagents. To
  exercise that part of superpowers' kit, the next experiment needs a task
  with naturally parallelizable subproblems (multiple independent modules,
  cross-cutting analysis).
- **Tasks with deeper specs.** A 6-test visible set against a 22-test
  held-out set is one calibration. A 1-test visible set or a 50-test
  held-out set would tilt the trade-off differently.
- **Other models.** All runs used the default model on this machine. The
  cost ratio scales differently for different models.

## Reproducing

```sh
cd experiments/correctness-comparison
uv run python run.py --reps 5
uv run python analyze.py
```

Workdirs and transcripts land in `results/` (gitignored).
