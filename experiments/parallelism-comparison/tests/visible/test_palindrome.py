from palindrome import is_palindrome


def test_simple_palindrome():
    assert is_palindrome("racecar")


def test_not_palindrome():
    assert not is_palindrome("hello")
