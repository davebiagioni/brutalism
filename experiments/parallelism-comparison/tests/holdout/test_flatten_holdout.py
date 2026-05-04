from flatten import flatten


def test_empty():
    assert flatten([]) == []


def test_deeply_nested():
    assert flatten([1, [2, [3, [4, [5]]]]]) == [1, 2, 3, 4, 5]


def test_strings_not_flattened():
    assert flatten(["ab", ["cd"]]) == ["ab", "cd"]


def test_tuples_not_flattened():
    # Only `list` is treated as nestable.
    assert flatten([(1, 2), [3, 4]]) == [(1, 2), 3, 4]


def test_empty_sublists_dropped():
    assert flatten([1, [], [2, []], 3]) == [1, 2, 3]


def test_preserves_order():
    assert flatten([[3, 1], [4, 1, 5], [9, 2, 6]]) == [3, 1, 4, 1, 5, 9, 2, 6]
