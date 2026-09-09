from src.guest.n010_hardware.n020_arithmetic.n020_FullAdder import FullAdder
from src.host.trusted_base import Bit


def test_FullAdder_truth_table():
    result, carry = FullAdder(Bit(0), Bit(0), Bit(0))
    assert result.value == 0
    assert carry.value == 0

    result, carry = FullAdder(Bit(0), Bit(0), Bit(1))
    assert result.value == 1
    assert carry.value == 0

    result, carry = FullAdder(Bit(0), Bit(1), Bit(0))
    assert result.value == 1
    assert carry.value == 0

    result, carry = FullAdder(Bit(0), Bit(1), Bit(1))
    assert result.value == 0
    assert carry.value == 1

    result, carry = FullAdder(Bit(1), Bit(0), Bit(0))
    assert result.value == 1
    assert carry.value == 0

    result, carry = FullAdder(Bit(1), Bit(0), Bit(1))
    assert result.value == 0
    assert carry.value == 1

    result, carry = FullAdder(Bit(1), Bit(1), Bit(0))
    assert result.value == 0
    assert carry.value == 1

    result, carry = FullAdder(Bit(1), Bit(1), Bit(1))
    assert result.value == 1
    assert carry.value == 1
