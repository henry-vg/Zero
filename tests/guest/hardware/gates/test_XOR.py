from src.guest.hardware.gates.XOR import XOR
from src.host.kernel.bit import Bit


def test_XOR_truth_table():
    assert XOR(Bit(0), Bit(0)).value == 0
    assert XOR(Bit(0), Bit(1)).value == 1
    assert XOR(Bit(1), Bit(0)).value == 1
    assert XOR(Bit(1), Bit(1)).value == 0
