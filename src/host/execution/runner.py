import shutil
from dataclasses import fields
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
    print("\033[2mRunning...\033[0m")
    with collect_metrics() as metrics:
        started_at = perf_counter_ns()

        try:
            output = program()

        except Exception as e:
            output = f"\033[1;31m[FATAL]\033[0m {e}"

        elapsed_ns = perf_counter_ns() - started_at
        terminal_width = shutil.get_terminal_size().columns

        guest_metrics = {
            field.metadata.get("label", field.name): getattr(metrics, field.name)
            for field in fields(metrics)
        }
        host_metrics = {
            "Time Elapsed": _format_duration(elapsed_ns),
        }
        metrics_width = max(map(len, guest_metrics.keys() | host_metrics.keys()))

    return "\n".join(
        [
            f"\033[96m{' OUTPUT '.center(terminal_width, '─')}\033[0m",
            output,
            f"\033[96m{' METRICS '.center(terminal_width, '─')}\033[0m",
            "\033[1;33mGUEST\033[0m",
            *(
                f"  {name + ':':<{metrics_width + 1}} \033[32m{value}\033[0m"
                for name, value in guest_metrics.items()
            ),
            "\033[1;33mHOST\033[0m",
            *(
                f"  {name + ':':<{metrics_width + 1}} \033[32m{value}\033[0m"
                for name, value in host_metrics.items()
            ),
            f"\033[96m{'─' * terminal_width}\033[0m",
        ]
    )
