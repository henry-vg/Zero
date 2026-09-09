from src.guest.n010_hardware.n010_gates.n030_OR import OR
from src.guest.n010_hardware.n020_arithmetic.n010_HalfAdder import HalfAdder
from src.host.trusted_base import Bit


def FullAdder(
    a: Bit,
    b: Bit,
    carry_in: Bit,
) -> tuple[Bit, Bit]:
    first_sum, first_carry = HalfAdder(a, b)
    result, second_carry = HalfAdder(first_sum, carry_in)
    carry_out = OR(first_carry, second_carry)

    return (
        result,
        carry_out,
    )
