from src.guest.n010_hardware.n010_gates.n040_XOR import XOR
from src.host.trusted_base import Bit


def test_XOR_truth_table():
    assert XOR(Bit(0), Bit(0)).value == 0
    assert XOR(Bit(0), Bit(1)).value == 1
    assert XOR(Bit(1), Bit(0)).value == 1
    assert XOR(Bit(1), Bit(1)).value == 0
