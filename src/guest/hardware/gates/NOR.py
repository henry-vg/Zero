from src.guest.hardware.gates.NOT import NOT
from src.guest.hardware.gates.OR import OR
from src.host.kernel.bit import Bit


def NOR(
    a: Bit,
    b: Bit,
) -> Bit:
    return NOT(OR(a, b))
