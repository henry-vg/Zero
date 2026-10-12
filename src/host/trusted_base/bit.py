from typing import Literal

from src.host.execution.metrics import count_calls_metric


class Bit:
    @count_calls_metric("bit_instances")
    def __init__(
        self,
        value: Literal[0, 1],
    ) -> None:
        if type(value) is not int or value not in (0, 1):
            raise ValueError("'Bit' value must be 0 or 1")

        self.value = value

    def __repr__(
        self,
    ) -> str:
        return f"Bit({self.value})"
