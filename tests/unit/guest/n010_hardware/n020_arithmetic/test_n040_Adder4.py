from src.guest.n010_hardware.n020_arithmetic.n040_Adder4 import Adder4
from src.host.trusted_base import Bit


def _assert_Adder4(
    a_0: int,
    a_1: int,
    a_2: int,
    a_3: int,
    b_0: int,
    b_1: int,
    b_2: int,
    b_3: int,
    expected_result_0: int,
    expected_result_1: int,
    expected_result_2: int,
    expected_result_3: int,
    expected_carry_out: int,
) -> None:
    result_0, result_1, result_2, result_3, carry_out = Adder4(
        Bit(a_0),
        Bit(a_1),
        Bit(a_2),
        Bit(a_3),
        Bit(b_0),
        Bit(b_1),
        Bit(b_2),
        Bit(b_3),
    )

    assert result_0.value == expected_result_0
    assert result_1.value == expected_result_1
    assert result_2.value == expected_result_2
    assert result_3.value == expected_result_3
    assert carry_out.value == expected_carry_out


def test_Adder4_partial_truth_table():
    _assert_Adder4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    _assert_Adder4(0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1)
    _assert_Adder4(0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0)
    _assert_Adder4(0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0)
    _assert_Adder4(0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0)
    _assert_Adder4(0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0)
    _assert_Adder4(0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1)
    _assert_Adder4(0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0)
    _assert_Adder4(0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0)
    _assert_Adder4(1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0)
    _assert_Adder4(1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1)
    _assert_Adder4(1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0)
    _assert_Adder4(1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0)
    _assert_Adder4(1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0)
    _assert_Adder4(1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1)
    _assert_Adder4(1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1)
