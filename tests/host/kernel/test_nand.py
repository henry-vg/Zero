from src.host.kernel.bit import Bit
from src.host.kernel.nand import nand


def test_nand_truth_table():
    assert nand(Bit(0), Bit(0)).value == 1
    assert nand(Bit(0), Bit(1)).value == 1
    assert nand(Bit(1), Bit(0)).value == 1
    assert nand(Bit(1), Bit(1)).value == 0
