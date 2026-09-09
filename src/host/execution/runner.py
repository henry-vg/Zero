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
) -> None:
    terminal_width = shutil.get_terminal_size().columns

    with collect_metrics() as metrics:
        print("Running...")
        print(" OUTPUT ".center(terminal_width, "─"))

        started_at = perf_counter_ns()

        try:
            print(program())

        except Exception as e:
            print(f"[FATAL] {e}")

        finally:
            elapsed_ns = perf_counter_ns() - started_at

            print(" METRICS ".center(terminal_width, "─"))
            print("GUEST")
            print(f"  BIT instances  {metrics.bit_instances}")
            print(f"  NAND calls     {metrics.nand_calls}")
            print("HOST")
            print(f"  Elapsed        {_format_duration(elapsed_ns)}")
            print("─" * terminal_width)
