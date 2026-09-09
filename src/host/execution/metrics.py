from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from functools import wraps
from typing import (
    Callable,
    ParamSpec,
    TypeVar,
)

P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class ExecutionMetrics:
    nand_calls: int = 0


_current_metrics: ContextVar[ExecutionMetrics | None] = ContextVar(
    "current_metrics",
    default=None,
)


@contextmanager
def collect_metrics() -> Generator[ExecutionMetrics]:
    metrics = ExecutionMetrics()
    token = _current_metrics.set(metrics)

    try:
        yield metrics
    finally:
        _current_metrics.reset(token)


def count_metric(
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
            metrics = _current_metrics.get()

            if metrics is not None:
                setattr(
                    metrics,
                    metric,
                    getattr(metrics, metric) + 1,
                )

            return function(*args, **kwargs)

        return wrapper

    return decorator
