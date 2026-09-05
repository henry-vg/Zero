from src.host.kernel.bit import Bit
from src.host.kernel.NAND import NAND


def NOT(
    a: Bit,
) -> Bit:
    return NAND(a, a)
