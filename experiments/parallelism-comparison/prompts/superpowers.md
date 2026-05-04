Read `task.md` and the failing tests in `tests/`.

Implement `palindrome.py`, `fibonacci.py`, `flatten.py`, and `roman.py` so
all visible tests pass.

The four modules are independent — they share nothing. Apply the **superpowers
test-driven-development** skill: red-green-refactor discipline, brainstorm
edge cases beyond the visible tests, watch each test fail before making it
pass, verify before completion. Use whatever superpowers subagents and skills
the workflow recommends — including `dispatching-parallel-agents` if
appropriate for independent subtasks.

Run `python -m pytest tests/ -q` to confirm. Stop when green.
