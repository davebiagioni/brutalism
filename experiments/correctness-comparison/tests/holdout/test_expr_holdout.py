"""Held-out correctness tests. Agents do not see this file during the run."""
import pytest
from expr import evaluate


# --- whitespace and trivial inputs ---

def test_whitespace_ignored():
    assert evaluate(" 1 + 2 ") == 3


def test_whitespace_inside_tokens():
    assert evaluate("1  +  2  *  3") == 7


def test_empty_raises():
    with pytest.raises(ValueError):
        evaluate("")


def test_whitespace_only_raises():
    with pytest.raises(ValueError):
        evaluate("   ")


# --- unary minus ---

def test_unary_minus_literal():
    assert evaluate("-3") == -3


def test_unary_minus_in_expression():
    assert evaluate("4 + -3") == 1


def test_unary_minus_chained():
    assert evaluate("--3") == 3


def test_leading_plus_ok():
    assert evaluate("+5") == 5


# --- power: right-associative, tighter than unary minus ---

def test_power_right_associative():
    assert evaluate("2**3**2") == 512


def test_power_tighter_than_unary_minus():
    assert evaluate("-2**2") == -4


def test_power_tighter_than_mul():
    assert evaluate("2*3**2") == 18


# --- modulo ---

def test_modulo_basic():
    assert evaluate("10%3") == 1


def test_modulo_precedence_with_add():
    assert evaluate("2+10%3") == 3


# --- division semantics ---

def test_division_exact_returns_float():
    assert evaluate("4/2") == 2.0
    assert isinstance(evaluate("4/2"), float)


def test_int_mul_returns_int():
    assert evaluate("3*4") == 12
    assert isinstance(evaluate("3*4"), int)


# --- error cases ---

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate("1/0")


def test_modulo_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate("5%0")


def test_unmatched_open_paren_raises():
    with pytest.raises(ValueError):
        evaluate("(1+2")


def test_unmatched_close_paren_raises():
    with pytest.raises(ValueError):
        evaluate("1+2)")


def test_garbage_token_raises():
    with pytest.raises(ValueError):
        evaluate("1 @ 2")


# --- nesting and decimals ---

def test_nested_parens():
    assert evaluate("((1+2)*3)+(4-1)") == 12


def test_float_literal():
    assert evaluate("1.5 + 2.5") == 4.0
