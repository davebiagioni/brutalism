# Task: LRU Cache

Implement an LRU (Least Recently Used) cache in `lru.py` so the existing tests
in `tests/test_lru.py` pass.

## API

```python
class LRUCache:
    def __init__(self, capacity: int): ...
    def get(self, key) -> value | None: ...   # returns None if absent
    def put(self, key, value) -> None: ...    # inserts or updates
```

Both `get` and `put` count as "uses" — they refresh recency.
When `put` would exceed capacity, evict the least-recently-used entry.

## Verifying

```
python -m pytest tests/test_lru.py -q
```

Tests must pass. That's the contract.
