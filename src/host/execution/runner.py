import shutil
from time import perf_counter_ns
from typing import Callable

from src.host.execution.metrics import collect_metrics


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


def run(
    program: Callable[[], str],
) -> str:
    print("Running...")
    with collect_metrics() as metrics:
        started_at = perf_counter_ns()

        try:
            output = program()

        except Exception as e:
            output = f"[FATAL] {e}"

        elapsed_ns = perf_counter_ns() - started_at
        terminal_width = shutil.get_terminal_size().columns

    return "\n".join(
        [
            " OUTPUT ".center(terminal_width, "─"),
            output,
            " METRICS ".center(terminal_width, "─"),
            "GUEST",
            *(f"  {name}: {value}" for name, value in vars(metrics).items()),
            "HOST",
            f"  time_elapsed: {_format_duration(elapsed_ns)}",
            "─" * terminal_width,
        ]
    )
