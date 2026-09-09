from src.host.execution.metrics import count_metric
from src.host.trusted_base.bit import Bit


@count_metric("nand_calls")
def NAND(
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
