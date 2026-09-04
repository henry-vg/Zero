from src.host.kernel.bit import Bit
from src.host.kernel.nand import nand


def main() -> None:
    a = Bit(1)
    b = Bit(0)

    result = nand(a, b)

    print(f"a    = {a}")
    print(f"b    = {b}")
    print(f"NAND = {result}")


if __name__ == "__main__":
    main()
