from src.host.execution import runner
from src.host.trusted_base import (
    NAND,
    Bit,
)


def test_format_duration():
    assert runner._format_duration(999) == "999 ns"
    assert runner._format_duration(1_000) == "1.00 µs"
    assert runner._format_duration(1_000_000) == "1.00 ms"
    assert runner._format_duration(1_000_000_000) == "1.00 s"


def test_run():
    def program() -> str:
        return repr(NAND(Bit(1), Bit(1)))

    output = runner.run(program)

    assert "Bit(0)" in output
    assert "bit_instances: 3" in output
    assert "nand_calls: 1" in output
    assert "time_elapsed:" in output


def test_run_reports_exception():
    def program() -> str:
        raise RuntimeError("boom")

    output = runner.run(program)

    assert "[FATAL] boom" in output
    assert "bit_instances: 0" in output
    assert "nand_calls: 0" in output
    assert "time_elapsed:" in output
