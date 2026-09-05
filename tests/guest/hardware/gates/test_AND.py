from src.guest.hardware.gates.AND import AND
from src.host.kernel.bit import Bit


def test_AND_truth_table():
    assert AND(Bit(0), Bit(0)).value == 0
    assert AND(Bit(0), Bit(1)).value == 0
    assert AND(Bit(1), Bit(0)).value == 0
    assert AND(Bit(1), Bit(1)).value == 1
