from collections.abc import (
    Callable,
)
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from functools import wraps
from typing import Generator


@dataclass
class ExecutionMetrics:
    bit_instances: int = 0
    nand_calls: int = 0


_current_metrics: ContextVar[ExecutionMetrics | None] = ContextVar(
    "current_metrics",
    default=None,
)


@contextmanager
def collect_metrics() -> Generator[ExecutionMetrics, None, None]:
    metrics = ExecutionMetrics()
    token = _current_metrics.set(metrics)

    try:
        yield metrics
    finally:
        _current_metrics.reset(token)


def count_metric[**P, R](
    metric: str,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(
        function: Callable[P, R],
    ) -> Callable[P, R]:
        @wraps(function)
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> R:
            result = function(*args, **kwargs)

            metrics = _current_metrics.get()

            if metrics is not None:
                setattr(
                    metrics,
                    metric,
                    getattr(metrics, metric) + 1,
                )

            return result

        return wrapper

    return decorator
