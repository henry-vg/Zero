from src.guest.hardware.gates.NOT import NOT
from src.host.kernel.bit import Bit


def test_NOT_truth_table():
    assert NOT(Bit(0)).value == 1
    assert NOT(Bit(1)).value == 0
