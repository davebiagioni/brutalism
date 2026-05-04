# Task: arithmetic expression evaluator

Implement `evaluate(expression: str) -> int | float` in `expr.py` so the
visible tests in `tests/test_expr.py` pass.

## Operators

| precedence (low → high) | operators  | associativity |
|-------------------------|------------|---------------|
| 1                       | `+` `-`    | left          |
| 2                       | `*` `/` `%`| left          |
| 3                       | `**`       | **right**     |
| 4                       | unary `-`  | right         |
| 5                       | `(` `)`    | —             |

- `/` always returns a float (e.g. `10 / 4 == 2.5`, `4 / 2 == 2.0`).
- `*` and `%` between integers return integers.
- `**` follows Python: `-2 ** 2 == -4` (power binds tighter than unary minus).
- Whitespace is ignored.
- Operands are integer or float literals (`12`, `3.14`).

## Errors

- Division or modulo by zero → `ZeroDivisionError`.
- Empty input, whitespace-only input, mismatched parens, or any malformed
  token sequence → `ValueError`.

## Verifying

```
python -m pytest tests/test_expr.py -q
```

Tests must pass. That's the contract.
