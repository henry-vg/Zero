import shutil
from dataclasses import fields
from typing import Callable

from src.host.execution.metrics import collect_execution_metrics


def run(program: Callable[[], str]) -> str:
    print("\033[2mRunning...\033[0m")

    with collect_execution_metrics() as metrics:
        try:
            output = program()
        except Exception as error:
            output = f"\033[1;31m[FATAL]\033[0m {error}"

    terminal_width = shutil.get_terminal_size().columns

    metric_groups = [
        (field_.name.upper(), getattr(metrics, field_.name))
        for field_ in fields(metrics)
    ]
    metrics_width = max(
        len(field_.metadata["label"])
        for _, group in metric_groups
        for field_ in fields(group)
    )

    return "\n".join(
        [
            f"\033[96m{' OUTPUT '.center(terminal_width, '─')}\033[0m",
            output,
            f"\033[96m{' METRICS '.center(terminal_width, '─')}\033[0m",
            *(
                line
                for name, group in metric_groups
                for line in (
                    f"\033[1;33m{name.upper()}\033[0m",
                    *(
                        f"  {label:<{metrics_width}} │ \033[32m{value}\033[0m"
                        for field_ in fields(group)
                        for label in (field_.metadata["label"],)
                        for value in (
                            field_.metadata["formatter"](getattr(group, field_.name)),
                        )
                    ),
                )
            ),
            f"\033[96m{'─' * terminal_width}\033[0m",
        ]
    )
