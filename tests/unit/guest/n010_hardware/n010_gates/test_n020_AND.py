from src.guest.n010_hardware.n010_gates.n020_AND import AND
from src.host.trusted_base.bit import Bit


def test_AND_truth_table():
    assert AND(Bit(0), Bit(0)).value == 0
    assert AND(Bit(0), Bit(1)).value == 0
    assert AND(Bit(1), Bit(0)).value == 0
    assert AND(Bit(1), Bit(1)).value == 1
