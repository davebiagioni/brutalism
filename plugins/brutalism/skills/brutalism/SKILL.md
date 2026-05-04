---
name: brutalism
description: Use ONLY when the user explicitly asks for brutalism — invokes /brutalize, says "be brutal", "brutalism mode", "brutalist style", or otherwise asks to strip code down. Do not auto-trigger on regular code tasks.
---

# Brutalism

Write code that does the job. Nothing else.

## Rules

1. Fewest lines that work.
2. No docstrings. No WHAT-comments — the code is the documentation. One-line WHY/invariant comments are allowed when the reason isn't derivable from reading the function (a non-obvious threshold, a hidden contract, a "returns None if...", a workaround for a specific quirk). If you can't say it in one line, the function is too long.
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
15. For N truly independent units of work, dispatch N comrades. Stay out of their way. Solo work is not a virtue.

## Testing

Tests exist. Tests pass. Non-negotiable.

1. Write the test first. Watch it fail.
2. Write the minimum code to pass it. Nothing more.
3. One assertion is enough if it proves the behavior. Brutally minimal is fine. Absent is not.
4. No mocks for things you control. No fixtures three layers deep.
5. If the test framework is heavy, vendor a 10-line runner.
6. Nothing ships without tests passing. No exceptions. The supreme leader demands results.

## Refactoring existing code

1. Read the file.
2. List what does not contribute to the requested behavior.
3. Remove it.
4. Run the tests. If none exist, write them first — see Testing.
5. Show the diff and the line-count delta.

## Limits

Functionality is preserved. Tests exist and pass. Public APIs other code depends on stay intact unless the user says otherwise.
