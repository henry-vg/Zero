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
    print("\033[2mRunning...\033[0m")
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
            f"\033[96m{' OUTPUT '.center(terminal_width, '─')}\033[0m",
            output,
            f"\033[96m{' METRICS '.center(terminal_width, '─')}\033[0m",
            "\033[1;33mGUEST\033[0m",
            *(
                f"  {name}: \033[32m{value}\033[0m"
                for name, value in vars(metrics).items()
            ),
            "\033[1;33mHOST\033[0m",
            f"  time_elapsed: \033[35m{_format_duration(elapsed_ns)}\033[0m",
            f"\033[96m{'─' * terminal_width}\033[0m",
        ]
    )
