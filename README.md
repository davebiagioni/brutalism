# brutalism

Claude Code plugin. The anti-superpowers plugin.

Writes code with minimal aesthetics and minimal extensibility. Gets it done in as few lines as possible.

## Why

You asked for a function. You got a sprint plan, a five-agent code review, a docstring with three examples, and a $1.20 bill. Capitalism writ in tool calls.

Brutalism gives you the function.

## Install

    /plugin marketplace add davebiagioni/brutalism
    /plugin install brutalism@brutalism
    /reload-plugins

## Use

- `/brutalism:brutalize <path>` — strip a file to its essentials. Lists what it will remove first, waits for confirmation.
- `/brutalism:depower` — audit `enabledPlugins` and turn off the ceremony-heavy ones (multi-agent reviewers, comprehensive frameworks, etc).

The skill is opt-in. It won't auto-apply to ordinary code tasks. Invoke a slash command, or say "be brutal" / "brutalism mode".

That's it.
