from src.guest.n010_hardware.n010_gates.n060_XNOR import XNOR
from src.host.trusted_base.bit import Bit


def test_XNOR_truth_table():
    assert XNOR(Bit(0), Bit(0)).value == 1
    assert XNOR(Bit(0), Bit(1)).value == 0
    assert XNOR(Bit(1), Bit(0)).value == 0
    assert XNOR(Bit(1), Bit(1)).value == 1
