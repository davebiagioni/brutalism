# brutalism

Claude Code plugin. The anti-superpowers plugin.

Writes code with minimal aesthetics and minimal extensibility. Gets it done in as few lines as possible.

## Why

You asked for a function. You got a sprint plan, a five-agent code review, a docstring with three examples, and a $1.20 bill. Capitalism writ in tool calls.

Brutalism gives you the function.

## Numbers

Three experiments. Same model, fresh sessions per run, N=5 each.

**LRU cache, fixed test suite.** Both produced the same 20-line implementation.

| metric         | brutalism | superpowers |
|----------------|----------:|------------:|
| wall time      |       14s |         35s |
| output tokens  |      1.3k |        5.7k |
| impl lines     |        20 |          20 |
| tests passed   |       6/6 |         6/6 |

**Expression evaluator, held-out edge tests.** Superpowers got one extra edge case at 5× the code.

| metric              | brutalism | superpowers |
|---------------------|----------:|------------:|
| wall time           |       35s |        123s |
| output tokens       |      4.7k |         30k |
| impl lines          |        25 |         134 |
| held-out correctness| 20.4/22   | 21.0/22     |

**Four independent micro-utilities.** Brutalism dispatched a comrade per module — exactly 4, every rep. Superpowers, with the same capability available, dispatched 1.6 times on average with stdev 2.2.

| metric                | brutalism | superpowers |
|-----------------------|----------:|------------:|
| wall time             |       49s |        135s |
| output tokens         |      15k  |         27k |
| impl lines            |        21 |          40 |
| held-out correctness  |    26/26  |      26/26  |
| `Agent` dispatches    | **4.0 ± 0** | 1.6 ± 2.2 |

A rule beats a menu on consistency. Brutalism does what it says. Across 30 runs total, superpowers won correctness once, by one test, in one experiment. Reproduction and full writeups: [`experiments/`](experiments/).

## Install

    /plugin marketplace add davebiagioni/brutalism
    /plugin install brutalism@brutalism
    /reload-plugins

## Use

- `/brutalism:brutalize <path>` — strip a file to its essentials. Lists what it will remove first, waits for confirmation.
- `/brutalism:depower` — audit `enabledPlugins` and turn off the ceremony-heavy ones (multi-agent reviewers, comprehensive frameworks, etc).

The skill is opt-in. It won't auto-apply to ordinary code tasks. Invoke a slash command, or say "be brutal" / "brutalism mode".

That's it.

---

<sub><img src="assets/engineering-center.jpg" width="320" alt="Engineering Center, University of Colorado Boulder — a brutalist concrete building"><br>Engineering Center, University of Colorado Boulder. The author wrote his thesis inside it. Photo by <a href="https://www.flickr.com/photos/jjes84/55029487863/">Jesse James</a>, <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>, via <a href="https://commons.wikimedia.org/wiki/File:Engineering_Center_CU_Boulder_(55029487863).jpg">Wikimedia Commons</a>. Resized.</sub>
