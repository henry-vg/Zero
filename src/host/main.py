from src.guest.n010_hardware.n020_arithmetic.n040_Adder4 import Adder4
from src.host.execution.runner import run
from src.host.trusted_base import Bit


def main() -> str:
    r_0, r_1, r_2, r_3, c = Adder4(
        Bit(1),
        Bit(0),
        Bit(0),
        Bit(1),
        Bit(1),
        Bit(0),
        Bit(1),
        Bit(0),
    )

    return "\n".join(
        [
            f"c   = {c}",
            f"r_3 = {r_3}",
            f"r_2 = {r_2}",
            f"r_1 = {r_1}",
            f"r_0 = {r_0}",
        ]
    )


if __name__ == "__main__":
    try:
        run(main)
    except Exception as e:
        print(f"[FATAL] {e}")
