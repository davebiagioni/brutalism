# Results: brutalism vs. superpowers on a fixed test suite

**Setup.** Toy task: implement an LRU cache (`task.md`) so the 6 fixed pytest
tests in `tests/test_lru.py` pass. Each arm runs in a fresh workdir via
`claude -p --session-id …`, with the arm-specific prompt as the only
deliberate difference. Model: default (whatever `claude` resolves on this
machine). N = 5 reps per arm.

## Numbers (mean ± stdev over 5 reps)

| metric              |   brutalism            |   superpowers          | ratio   |
|---------------------|-----------------------:|-----------------------:|--------:|
| tests pass          |                  5 / 5 |                  5 / 5 | —       |
| wall time (s)       |             14.1 ± 1.8 |             34.5 ± 7.1 | **2.4×** |
| assistant turns     |              7  ± 0.0  |             15  ± 3.3  | 2.1×    |
| output tokens       |          1,301 ± 20    |          5,726 ± 913   | **4.4×** |
| total input tokens  |        205,775 ± 6     |        476,722 ± 133k  | 2.3×    |
| tool calls          |              5  ± 0.0  |            8.6  ± 1.8  | 1.7×    |
| `Task` / subagent   |              0  ± 0.0  |              0  ± 0.0  | —       |
| impl lines          |             20  ± 0    |             20  ± 0    | 1×      |
| impl chars          |            507  ± 15   |            556  ± 0    | 1.10×   |

Tool mix (mean per run):

- brutalism: `Read=2.0, Bash=2.0, Write=1.0`
- superpowers: `Bash=5.2, Read=2.4, Write=1.0`

## Read

1. **Both arms produce essentially the same code.** Same length, same
   `OrderedDict`-based approach. Style differences are cosmetic: type hints,
   `_data` underscore.
2. **Superpowers' overhead here is process, not parallelism.** Zero subagent
   calls in either arm. Superpowers' extra cost shows up as iterative test
   execution (5.2 vs 2.0 `Bash` calls) and verbalized planning in the output
   stream (4.4× output tokens).
3. **Brutalism is shockingly deterministic.** 7 turns and 5 tool calls in
   every single rep; output token stdev is ±20 across 5 samples. It executes
   a fixed playbook: read task, read tests, write file, run pytest, stop.
4. **Superpowers carries real variance.** Wall stdev ≈20% of the mean; cache
   token stdev ≈28% of the mean. The TDD skill's branching adds genuine
   sampling variation.

## What this experiment does NOT show

The task is too small to need subagents and too easy to get wrong. Both arms
produced correct code, so the 2.4× wall-time ratio is pure overhead **for
this problem class**. To see whether superpowers' extra process pays off, the
next experiment needs:

- A task with subtle edge cases the visible tests don't cover.
- A held-out correctness check, so "passes the tests" can diverge from "is
  actually correct".
- Optionally, more surface area so subagent dispatching has something to do.

## Reproducing

```sh
cd experiments/tdd-comparison
uv run python run.py --reps 5
uv run python analyze.py
```

Raw transcripts and per-rep workdirs land in `results/` (gitignored).
