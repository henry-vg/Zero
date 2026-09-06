from src.guest.n010_hardware.n010_gates.n010_NOT import NOT
from src.guest.n010_hardware.n010_gates.n040_XOR import XOR
from src.host.trusted_base.bit import Bit


def XNOR(
    a: Bit,
    b: Bit,
) -> Bit:
    return NOT(XOR(a, b))
