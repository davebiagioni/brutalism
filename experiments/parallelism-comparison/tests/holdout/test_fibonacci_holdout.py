import pytest
from fibonacci import fib


def test_fib_2():
    assert fib(2) == 1


def test_fib_20():
    assert fib(20) == 6765


def test_fib_50():
    assert fib(50) == 12586269025


def test_fib_negative_raises():
    with pytest.raises(ValueError):
        fib(-1)


def test_fib_large_efficient():
    # If implemented naively recursive, this will time out.
    assert fib(100) == 354224848179261915075
