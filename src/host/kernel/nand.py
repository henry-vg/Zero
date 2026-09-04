from src.host.kernel.bit import Bit


def nand(
    a: Bit,
    b: Bit,
) -> Bit:
    table = {
        (0, 0): 1,
        (0, 1): 1,
        (1, 0): 1,
        (1, 1): 0,
    }
    return Bit(table[(a.value, b.value)])
