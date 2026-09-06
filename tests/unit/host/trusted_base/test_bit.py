import pytest
from src.host.trusted_base import Bit


def test_bit_accepts_zero():
    bit = Bit(0)

    assert bit.value == 0


def test_bit_accepts_one():
    bit = Bit(1)

    assert bit.value == 1


def test_bit_repr():
    bit = Bit(0)

    assert repr(bit) == "Bit(0)"


def test_bit_rejects_invalid_value():
    with pytest.raises(ValueError):
        Bit(2)


def test_bit_rejects_bool():
    with pytest.raises(ValueError):
        Bit(True)
