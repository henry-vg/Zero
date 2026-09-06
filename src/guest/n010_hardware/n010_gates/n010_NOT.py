from src.host.trusted_base.bit import Bit
from src.host.trusted_base.NAND import NAND


def NOT(
    a: Bit,
) -> Bit:
    return NAND(a, a)
