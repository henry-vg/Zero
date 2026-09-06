from src.guest.n010_hardware.n010_gates.n010_NOT import NOT
from src.host.trusted_base import (
    NAND,
    Bit,
)


def AND(
    a: Bit,
    b: Bit,
) -> Bit:
    return NOT(NAND(a, b))
