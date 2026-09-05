from src.guest.n010_hardware.n010_gates.n010_NOT import NOT
from src.host.kernel.bit import Bit
from src.host.kernel.NAND import NAND


def OR(
    a: Bit,
    b: Bit,
) -> Bit:
    return NAND(
        NOT(a),
        NOT(b),
    )
