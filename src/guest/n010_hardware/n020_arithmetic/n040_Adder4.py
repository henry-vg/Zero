from src.guest.n010_hardware.n020_arithmetic.n020_FullAdder import FullAdder
from src.guest.n010_hardware.n020_arithmetic.n030_Adder2 import Adder2
from src.host.trusted_base import Bit


def Adder4(
    a_0: Bit,
    a_1: Bit,
    a_2: Bit,
    a_3: Bit,
    b_0: Bit,
    b_1: Bit,
    b_2: Bit,
    b_3: Bit,
) -> tuple[Bit, Bit, Bit, Bit, Bit]:
    result_0, result_1, carry_2 = Adder2(
        a_0,
        a_1,
        b_0,
        b_1,
    )
    result_2, carry_3 = FullAdder(a_2, b_2, carry_2)
    result_3, carry_out = FullAdder(a_3, b_3, carry_3)

    return (
        result_0,
        result_1,
        result_2,
        result_3,
        carry_out,
    )
