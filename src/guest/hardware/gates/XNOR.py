from src.guest.hardware.gates.NOT import NOT
from src.guest.hardware.gates.XOR import XOR
from src.host.kernel.bit import Bit


def XNOR(
    a: Bit,
    b: Bit,
) -> Bit:
    return NOT(XOR(a, b))
