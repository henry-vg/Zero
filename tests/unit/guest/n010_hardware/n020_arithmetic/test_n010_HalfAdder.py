from src.guest.n010_hardware.n020_arithmetic.n010_HalfAdder import HalfAdder
from src.host.trusted_base import Bit


def test_HalfAdder_truth_table():
    result, carry = HalfAdder(Bit(0), Bit(0))
    assert result.value == 0
    assert carry.value == 0

    result, carry = HalfAdder(Bit(0), Bit(1))
    assert result.value == 1
    assert carry.value == 0

    result, carry = HalfAdder(Bit(1), Bit(0))
    assert result.value == 1
    assert carry.value == 0

    result, carry = HalfAdder(Bit(1), Bit(1))
    assert result.value == 0
    assert carry.value == 1
