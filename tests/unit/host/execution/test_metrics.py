import pytest
from src.host.execution import metrics


def test_format_duration():
    assert metrics._format_duration(999) == "999 ns"
    assert metrics._format_duration(1_000) == "1.00 µs"
    assert metrics._format_duration(1_000_000) == "1.00 ms"
    assert metrics._format_duration(1_000_000_000) == "1.00 s"


def test_count_calls_metric():
    @metrics.count_calls_metric("nand_calls")
    def operation() -> str:
        return "done"

    with metrics.collect_execution_metrics() as execution_metrics:
        assert operation() == "done"

    assert execution_metrics.guest.nand_calls == 1


def test_collect_execution_metrics(monkeypatch):
    timestamps = iter((100, 125))
    monkeypatch.setattr(metrics, "perf_counter_ns", lambda: next(timestamps))

    with metrics.collect_execution_metrics() as execution_metrics:
        pass

    assert execution_metrics.host.elapsed_time_ns == 25


def test_collect_execution_metrics_on_error(monkeypatch):
    timestamps = iter((100, 125))
    monkeypatch.setattr(metrics, "perf_counter_ns", lambda: next(timestamps))

    with pytest.raises(RuntimeError, match="failed"):
        with metrics.collect_execution_metrics() as execution_metrics:
            raise RuntimeError("failed")

    assert execution_metrics.host.elapsed_time_ns == 25


def test_collect_execution_metrics_restores_outer_context():
    @metrics.count_calls_metric("nand_calls")
    def operation() -> None:
        pass

    with metrics.collect_execution_metrics() as outer:
        operation()

        with metrics.collect_execution_metrics() as inner:
            operation()

        operation()

    assert outer.guest.nand_calls == 2
    assert inner.guest.nand_calls == 1
