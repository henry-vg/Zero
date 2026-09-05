from src.host.kernel.bit import Bit
from src.host.kernel.nand import nand


def main() -> str:
    a = Bit(1)
    b = Bit(0)

    result = nand(a, b)

    return "\n".join(
        [
            f"a    = {a}",
            f"b    = {b}",
            f"NAND = {result}",
        ]
    )


if __name__ == "__main__":
    try:
        print(main())
    except Exception as e:
        print(f"[FATAL] {e}")
