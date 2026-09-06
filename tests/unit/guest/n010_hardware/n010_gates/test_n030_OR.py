from src.guest.n010_hardware.n010_gates.n030_OR import OR
from src.host.trusted_base import Bit


def test_OR_truth_table():
    assert OR(Bit(0), Bit(0)).value == 0
    assert OR(Bit(0), Bit(1)).value == 1
    assert OR(Bit(1), Bit(0)).value == 1
    assert OR(Bit(1), Bit(1)).value == 1
