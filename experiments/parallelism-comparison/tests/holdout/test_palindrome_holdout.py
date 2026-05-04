import pytest
from palindrome import is_palindrome


def test_empty_string():
    assert is_palindrome("")


def test_single_char():
    assert is_palindrome("x")


def test_case_insensitive():
    assert is_palindrome("RaceCar")


def test_ignore_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama")


def test_ignore_spaces():
    assert is_palindrome("taco cat")


def test_alphanumeric_palindrome():
    assert is_palindrome("12321")


def test_mixed_letters_digits():
    assert is_palindrome("a1b2b1a")


def test_unicode_letters_not_required():
    assert is_palindrome("hello-olleh")
