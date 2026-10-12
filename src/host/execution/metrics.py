from collections.abc import (
    Callable,
    Generator,
)
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import (
    Field,
    dataclass,
    field,
)
from functools import wraps
from time import perf_counter_ns


def _format_duration(
    nanoseconds: int,
) -> str:
    if nanoseconds < 1_000:
        return f"{nanoseconds} ns"
    if nanoseconds < 1_000_000:
        return f"{nanoseconds / 1_000:.2f} µs"
    if nanoseconds < 1_000_000_000:
        return f"{nanoseconds / 1_000_000:.2f} ms"
    return f"{nanoseconds / 1_000_000_000:.2f} s"


def _metric(
    label: str,
    formatter: Callable[[int], str] = str,
) -> Field[int]:
    return field(
        default=0,
        metadata={
            "label": label,
            "formatter": formatter,
        },
    )


@dataclass
class GuestMetrics:
    bit_instances: int = _metric("Bit Instances")
    nand_calls: int = _metric("NAND Calls")


@dataclass
class HostMetrics:
    elapsed_time_ns: int = _metric("Elapsed Time", _format_duration)


@dataclass
class ExecutionMetrics:
    guest: GuestMetrics = field(default_factory=GuestMetrics)
    host: HostMetrics = field(default_factory=HostMetrics)


_current_metrics: ContextVar[ExecutionMetrics | None] = ContextVar(
    "current_metrics",
    default=None,
)


def count_calls_metric[**P, R](
    metric_name: str,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            execution_metrics = _current_metrics.get()

            if execution_metrics is not None:
                guest_metrics = execution_metrics.guest
                setattr(
                    guest_metrics,
                    metric_name,
                    getattr(guest_metrics, metric_name) + 1,
                )
            return result

        return wrapper

    return decorator


@contextmanager
def collect_execution_metrics() -> Generator[ExecutionMetrics, None, None]:
    metrics = ExecutionMetrics()
    token = _current_metrics.set(metrics)
    started_at = perf_counter_ns()

    try:
        yield metrics
    finally:
        metrics.host.elapsed_time_ns = perf_counter_ns() - started_at
        _current_metrics.reset(token)
