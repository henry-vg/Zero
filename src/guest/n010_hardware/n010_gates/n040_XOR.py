from src.host.trusted_base import (
    NAND,
    Bit,
)


def XOR(
    a: Bit,
    b: Bit,
) -> Bit:
    a_nand_b = NAND(a, b)

    return NAND(
        NAND(a, a_nand_b),
        NAND(b, a_nand_b),
    )
