---
name: brutalism
description: Use ONLY when the user explicitly asks for brutalism — invokes /brutalize, says "be brutal", "brutalism mode", "brutalist style", or otherwise asks to strip code down. Do not auto-trigger on regular code tasks.
---

# Brutalism

Write code that does the job. Nothing else.

## Rules

1. Fewest lines that work.
2. No comments. No docstrings. The code is the documentation.
3. No helper used once. Inline it.
4. No abstraction for hypothetical futures. No interface with one implementer.
5. No error handling for cases that cannot happen. Let it crash at boundaries you don't own.
6. No logging unless the user asked for it.
7. No config flags unless the user asked for it.
8. No banners, boxes, emojis, or pretty-printed output.
9. Collapse trivial classes to functions. Collapse trivial modules to a file.
10. Prefer the standard library. A new dependency must save more lines than it costs.
11. Short names in short scopes. Long names only when scope demands it.
12. No `try/except` that just re-raises or logs.
13. Delete dead code, unused params, and `# TODO` for things you won't do.
14. If a feature wasn't requested, don't build it.

## Refactoring existing code

1. Read the file.
2. List what does not contribute to the requested behavior.
3. Remove it.
4. Run tests if they exist.
5. Show the diff and the line-count delta.

## Limits

Functionality is preserved. Tests still pass. Public APIs other code depends on stay intact unless the user says otherwise.
