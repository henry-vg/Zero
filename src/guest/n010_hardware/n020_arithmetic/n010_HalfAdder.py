from src.guest.n010_hardware.n010_gates.n020_AND import AND
from src.guest.n010_hardware.n010_gates.n040_XOR import XOR
from src.host.trusted_base import Bit


def HalfAdder(
    a: Bit,
    b: Bit,
) -> tuple[Bit, Bit]:
    return (
        XOR(a, b),
        AND(a, b),
    )
