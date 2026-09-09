from src.guest.n010_hardware.n020_arithmetic.n010_HalfAdder import HalfAdder
from src.guest.n010_hardware.n020_arithmetic.n020_FullAdder import FullAdder
from src.host.trusted_base import Bit


def Adder2(
    a_0: Bit,
    a_1: Bit,
    b_0: Bit,
    b_1: Bit,
) -> tuple[Bit, Bit, Bit]:
    result_0, carry_0 = HalfAdder(a_0, b_0)
    result_1, carry_out = FullAdder(a_1, b_1, carry_0)

    return (
        result_0,
        result_1,
        carry_out,
    )
