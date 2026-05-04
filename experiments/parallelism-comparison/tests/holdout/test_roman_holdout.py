import pytest
from roman import to_roman


def test_subtractive_pairs():
    assert to_roman(40) == "XL"
    assert to_roman(90) == "XC"
    assert to_roman(400) == "CD"
    assert to_roman(900) == "CM"


def test_three_thousand_nine_hundred_ninety_nine():
    assert to_roman(3999) == "MMMCMXCIX"


def test_no_zero():
    with pytest.raises(ValueError):
        to_roman(0)


def test_no_negative():
    with pytest.raises(ValueError):
        to_roman(-5)


def test_too_large():
    with pytest.raises(ValueError):
        to_roman(4000)


def test_no_four_in_a_row():
    # Subtractive notation: 4 is IV, never IIII.
    assert to_roman(4) == "IV"
    assert "IIII" not in to_roman(4)


def test_powers_of_ten():
    assert to_roman(10) == "X"
    assert to_roman(100) == "C"
    assert to_roman(1000) == "M"
