from src.guest.hardware.gates.NOT import NOT
from src.host.kernel.bit import Bit
from src.host.kernel.NAND import NAND


def AND(
    a: Bit,
    b: Bit,
) -> Bit:
    return NOT(NAND(a, b))
