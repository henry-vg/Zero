from src.guest.n010_hardware.n030_selection.n010_Mux import Mux
from src.host.trusted_base import Bit


def _assert_Mux(
    a: int,
    b: int,
    select: int,
    expected_output: int,
) -> None:
    output = Mux(
        Bit(a),
        Bit(b),
        Bit(select),
    )

    assert output.value == expected_output


def test_Mux_truth_table():
    _assert_Mux(0, 0, 0, 0)
    _assert_Mux(0, 0, 1, 0)
    _assert_Mux(0, 1, 0, 0)
    _assert_Mux(0, 1, 1, 1)
    _assert_Mux(1, 0, 0, 1)
    _assert_Mux(1, 0, 1, 0)
    _assert_Mux(1, 1, 0, 1)
    _assert_Mux(1, 1, 1, 1)
