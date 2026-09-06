from src.host.trusted_base.bit import Bit
from src.host.trusted_base.NAND import NAND


def test_NAND_truth_table():
    assert NAND(Bit(0), Bit(0)).value == 1
    assert NAND(Bit(0), Bit(1)).value == 1
    assert NAND(Bit(1), Bit(0)).value == 1
    assert NAND(Bit(1), Bit(1)).value == 0
