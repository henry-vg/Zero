from src.guest.n010_hardware.n010_gates.n010_NOT import NOT
from src.guest.n010_hardware.n010_gates.n020_AND import AND
from src.guest.n010_hardware.n010_gates.n030_OR import OR
from src.host.trusted_base import Bit


def Mux(
    a: Bit,
    b: Bit,
    select: Bit,
) -> Bit:
    return OR(
        AND(a, NOT(select)),
        AND(b, select),
    )
