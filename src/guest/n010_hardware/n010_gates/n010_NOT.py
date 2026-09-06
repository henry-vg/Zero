from src.host.trusted_base import (
    NAND,
    Bit,
)


def NOT(
    a: Bit,
) -> Bit:
    return NAND(a, a)
