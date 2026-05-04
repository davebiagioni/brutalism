# Task: four independent micro-utilities

Implement four unrelated utilities, **each in its own module**, so the visible
tests in `tests/` pass.

## Modules

### `palindrome.py`

```python
def is_palindrome(s: str) -> bool: ...
```

True iff `s` reads the same forwards and backwards after lowercasing and
discarding non-alphanumeric characters. Empty string is a palindrome.

### `fibonacci.py`

```python
def fib(n: int) -> int: ...
```

Returns the n-th Fibonacci number with `fib(0) == 0`, `fib(1) == 1`. Must be
O(n) time and O(1) space (no naive recursion). `n < 0` raises `ValueError`.

### `flatten.py`

```python
def flatten(items) -> list: ...
```

Returns a flat list with every level of list-nesting removed. Treats only
`list` (not tuples or strings) as nestable. Order preserved.

### `roman.py`

```python
def to_roman(n: int) -> str: ...
```

Converts integers in `1..3999` to Roman numerals using subtractive notation
(`IV`, `IX`, `XL`, `XC`, `CD`, `CM`). Out-of-range raises `ValueError`.

## Verifying

```
python -m pytest tests/ -q
```

Tests must pass. That's the contract.
