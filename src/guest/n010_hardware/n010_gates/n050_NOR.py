from src.guest.n010_hardware.n010_gates.n010_NOT import NOT
from src.guest.n010_hardware.n010_gates.n030_OR import OR
from src.host.kernel.bit import Bit


def NOR(
    a: Bit,
    b: Bit,
) -> Bit:
    return NOT(OR(a, b))
