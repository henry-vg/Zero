from src.guest.hardware.gates.NOT import NOT
from src.host.kernel.bit import Bit
from src.host.kernel.NAND import NAND


def main() -> str:
    NAND_result = NAND(
        Bit(0),
        Bit(1),
    )

    NOT_result = NOT(
        Bit(0),
    )

    return "\n".join(
        [
            f"NAND = {NAND_result}",
            f"NOT = {NOT_result}",
        ]
    )


if __name__ == "__main__":
    try:
        print(main())
    except Exception as e:
        print(f"[FATAL] {e}")
