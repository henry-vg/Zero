from src.guest.hardware.gates.AND import AND
from src.guest.hardware.gates.NOR import NOR
from src.guest.hardware.gates.NOT import NOT
from src.guest.hardware.gates.OR import OR
from src.guest.hardware.gates.XNOR import XNOR
from src.guest.hardware.gates.XOR import XOR
from src.host.kernel.bit import Bit
from src.host.kernel.NAND import NAND


def main() -> str:
    NAND_result = NAND(Bit(1), Bit(1))
    AND_result = AND(Bit(1), Bit(1))
    NOR_result = NOR(Bit(1), Bit(1))
    NOT_result = NOT(Bit(1))
    OR_result = OR(Bit(1), Bit(1))
    XNOR_result = XNOR(Bit(1), Bit(1))
    XOR_result = XOR(Bit(1), Bit(1))

    return "\n".join(
        [
            f"NAND_result = {NAND_result}",
            f"AND_result  = {AND_result}",
            f"NOR_result  = {NOR_result}",
            f"NOT_result  = {NOT_result}",
            f"OR_result   = {OR_result}",
            f"XNOR_result = {XNOR_result}",
            f"XOR_result  = {XOR_result}",
        ]
    )


if __name__ == "__main__":
    try:
        print(main())
    except Exception as e:
        print(f"[FATAL] {e}")
