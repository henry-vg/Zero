from src.guest.hardware.gates.NOR import NOR
from src.host.kernel.bit import Bit


def test_NOR_truth_table():
    assert NOR(Bit(0), Bit(0)).value == 1
    assert NOR(Bit(0), Bit(1)).value == 0
    assert NOR(Bit(1), Bit(0)).value == 0
    assert NOR(Bit(1), Bit(1)).value == 0
