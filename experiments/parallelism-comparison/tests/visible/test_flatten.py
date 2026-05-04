from flatten import flatten


def test_flat_list_unchanged():
    assert flatten([1, 2, 3]) == [1, 2, 3]


def test_one_level_nested():
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]
