from src.guest.n010_hardware.n020_arithmetic.n030_Adder2 import Adder2
from src.host.trusted_base import Bit


def _assert_Adder2(
    a_0: int,
    a_1: int,
    b_0: int,
    b_1: int,
    expected_result_0: int,
    expected_result_1: int,
    expected_carry_out: int,
) -> None:
    result_0, result_1, carry_out = Adder2(
        Bit(a_0),
        Bit(a_1),
        Bit(b_0),
        Bit(b_1),
    )

    assert result_0.value == expected_result_0
    assert result_1.value == expected_result_1
    assert carry_out.value == expected_carry_out


def test_Adder2_truth_table():
    _assert_Adder2(0, 0, 0, 0, 0, 0, 0)
    _assert_Adder2(0, 0, 1, 0, 1, 0, 0)
    _assert_Adder2(0, 0, 0, 1, 0, 1, 0)
    _assert_Adder2(0, 0, 1, 1, 1, 1, 0)
    _assert_Adder2(1, 0, 0, 0, 1, 0, 0)
    _assert_Adder2(1, 0, 1, 0, 0, 1, 0)
    _assert_Adder2(1, 0, 0, 1, 1, 1, 0)
    _assert_Adder2(1, 0, 1, 1, 0, 0, 1)
    _assert_Adder2(0, 1, 0, 0, 0, 1, 0)
    _assert_Adder2(0, 1, 1, 0, 1, 1, 0)
    _assert_Adder2(0, 1, 0, 1, 0, 0, 1)
    _assert_Adder2(0, 1, 1, 1, 1, 0, 1)
    _assert_Adder2(1, 1, 0, 0, 1, 1, 0)
    _assert_Adder2(1, 1, 1, 0, 0, 0, 1)
    _assert_Adder2(1, 1, 0, 1, 1, 0, 1)
    _assert_Adder2(1, 1, 1, 1, 0, 1, 1)
