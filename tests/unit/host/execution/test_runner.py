from src.host.execution import metrics
from src.host.execution.runner import run


def test_run_rendering(monkeypatch):
    timestamps = iter((100, 125))
    monkeypatch.setattr(metrics, "perf_counter_ns", lambda: next(timestamps))

    @metrics.count_calls_metric("nand_calls")
    def program() -> str:
        return "done"

    output = run(program)

    assert "done" in output
    assert "\033[1;33mGUEST\033[0m" in output
    assert "  Bit Instances │ \033[32m0\033[0m" in output
    assert "  NAND Calls    │ \033[32m1\033[0m" in output
    assert "\033[1;33mHOST\033[0m" in output
    assert "  Elapsed Time  │ \033[32m25 ns\033[0m" in output


def test_run_rendering_on_error(monkeypatch):
    timestamps = iter((100, 125))
    monkeypatch.setattr(metrics, "perf_counter_ns", lambda: next(timestamps))

    def program() -> str:
        raise RuntimeError("boom")

    output = run(program)

    assert "\033[1;31m[FATAL]\033[0m boom" in output
    assert "  Bit Instances │ \033[32m0\033[0m" in output
    assert "  NAND Calls    │ \033[32m0\033[0m" in output
    assert "  Elapsed Time  │ \033[32m25 ns\033[0m" in output
