from src.guest.n010_hardware.n010_gates.n010_NOT import NOT
from src.host.trusted_base import Bit


def test_NOT_truth_table():
    assert NOT(Bit(0)).value == 1
    assert NOT(Bit(1)).value == 0
