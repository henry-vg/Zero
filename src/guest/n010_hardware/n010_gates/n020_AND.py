from src.guest.n010_hardware.n010_gates.n010_NOT import NOT
from src.host.trusted_base.bit import Bit
from src.host.trusted_base.NAND import NAND


def AND(
    a: Bit,
    b: Bit,
) -> Bit:
    return NOT(NAND(a, b))
