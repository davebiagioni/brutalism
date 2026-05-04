# Results: brutalism vs. superpowers on a parallelizable task

**Setup.** Implement four independent micro-utilities (`palindrome`,
`fibonacci`, `flatten`, `roman`), each in its own module. Visible tests check
happy paths; 26 held-out tests probe edges, error paths, and an O(n)
performance check on `fib(100)`. N = 5 reps per arm. Default model.

This run was made *after* adding **rule 15** to the brutalism skill:

> **15. For N truly independent units of work, dispatch N comrades. Stay
> out of their way. Solo work is not a virtue.**

The rule was also mirrored in the brutalism arm's prompt, since the user's
Claude Code env doesn't have the brutalism plugin installed and so wouldn't
load `SKILL.md` automatically.

## Numbers (mean ± stdev, N=5)

| metric                | brutalism (rule 15)    | superpowers            | ratio  |
|-----------------------|-----------------------:|-----------------------:|-------:|
| visible passed        |              8 / 8     |          30.4 / 30.4*  | —      |
| **held-out passed**   |        **26 / 26**     |        **26 / 26**     | tied   |
| **`Agent` calls**     |           **4.0 ± 0**  |          **1.6 ± 2.2** | 2.5×   |
| wall time (s)         |             48.7 ± 3.6 |          134.6 ± 71.3  | 2.8×   |
| assistant turns       |             17.6 ± 2.6 |             29.2 ± 5.3 | 1.7×   |
| output tokens         |     14,916 ± 1,445     |     26,599 ± 9,377     | 1.8×   |
| total input tokens    |    541,232 ± 85,677    |  1,075,544 ± 298,492   | 2.0×   |
| tool calls            |           12.6 ± 2.6   |             21 ± 4.5   | 1.7×   |
| impl lines            |           21.2 ± 4.6   |             40 ± 5.5   | 1.9×   |

*Superpowers wrote variable numbers of self-tests, padding the visible
count above 8.

## Read

1. **Brutalism kept its promise every single time. Superpowers did not.**
   Rule 15 says: dispatch N comrades for N independent units. Brutalism
   dispatched exactly 4, in every rep, stdev zero. Superpowers' kit
   *includes* `dispatching-parallel-agents` and the prompt explicitly
   permitted it — yet it dispatched 1.6 ± 2.2 times across reps (some 0,
   some more). A rule beats a menu on consistency.
2. **The headline is predictability, not parallelism.** Whether dispatch
   actually wins on wall time depends on subtask size; this experiment's
   subtasks are too small for parallelism to pay off (~24s sequential →
   ~49s with comrades). That's the cost of doing what you said you'd do.
   Adjust the rule's threshold if that trade isn't worth it for your work,
   but the *behavior is legible* either way.
3. **No correctness signal on this task.** Both arms got perfect held-out
   pass rates in every rep. The four micro-utilities are well-known; the
   model's priors handle them cleanly without process discipline.
4. **Code volume narrowed.** Superpowers' lead on impl lines dropped from
   5.3× (exp 2) to 1.9× here. With independent units and parallelism, the
   "verbalize a plan" overhead has fewer places to land.

## Why "rule beats menu" matters

A skill that lists capabilities ("you may use X if appropriate") asks the
model to make a judgment call every time. Judgment calls are noisy. A skill
that asserts a rule ("for N independent units, dispatch N comrades")
removes the judgment from the loop. The behavior becomes deterministic; the
operator knows what they bought. If the rule fires inappropriately for a
specific task, the operator can override in the prompt — but they only
have to override the cases they want to change, instead of *hoping* the
right behavior emerges.

This is a meta-finding worth more attention than the wall-time number.

## Cost vs. quality (across all three experiments)

| experiment              | held-out (b vs s)    | wall ratio | output token ratio | extra correctness |
|-------------------------|---------------------:|-----------:|-------------------:|------------------:|
| 1. tdd-comparison (LRU) |    6/6 vs 6/6        |       2.4× |               4.4× | none              |
| 2. correctness (expr)   |    20.4 vs 21.0 / 22 |       3.5× |               6.4× | +1 test           |
| 3. parallelism (4 utils)|    26/26 vs 26/26    |       2.8× |               1.8× | none              |

Across 30 total runs (15 per plugin), superpowers won correctness once, by
one test, in one experiment. The cost premium ranged from 1.8× to 6.4× in
output tokens.

## Caveats

- **Rule 15 is brand new.** This is the first run after adding it. We
  don't know how it interacts with adversarial tasks or with tasks where
  parallel dispatch is a trap.
- **N=5 is still small.** The Agent-call stdev of zero in brutalism is
  unusually clean — possibly a quirk of how the model interprets the rule's
  imperative ("dispatch N comrades") versus a permissive option.
- **Plugin loading caveat from earlier experiments still applies.** The
  brutalism skill is described inline in the prompt rather than auto-loaded.

## Reproducing

```sh
cd experiments/parallelism-comparison
uv run python run.py --reps 5
uv run python analyze.py
```
