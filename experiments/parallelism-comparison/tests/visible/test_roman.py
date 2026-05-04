from roman import to_roman


def test_basic_roman():
    assert to_roman(1) == "I"
    assert to_roman(4) == "IV"
    assert to_roman(9) == "IX"


def test_complex_roman():
    assert to_roman(1994) == "MCMXCIV"
