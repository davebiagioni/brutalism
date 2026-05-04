import pytest
from expr import evaluate


def test_addition():
    assert evaluate("1+2") == 3


def test_precedence_mul_over_add():
    assert evaluate("2*3+4") == 10


def test_parens_override_precedence():
    assert evaluate("(2+3)*4") == 20


def test_subtraction_left_associative():
    assert evaluate("10-3-2") == 5


def test_power_basic():
    assert evaluate("2**3") == 8


def test_division_returns_float():
    assert evaluate("10/4") == 2.5
