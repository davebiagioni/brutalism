from fibonacci import fib


def test_fib_zero():
    assert fib(0) == 0


def test_fib_small():
    assert fib(1) == 1
    assert fib(10) == 55
