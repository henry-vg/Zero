from src.host.execution.metrics import (
    collect_metrics,
    count_metric,
)
from src.host.trusted_base import (
    NAND,
    Bit,
)


def test_collect_metrics():
    with collect_metrics() as metrics:
        assert vars(metrics) == {
            "bit_instances": 0,
            "nand_calls": 0,
        }

        NAND(Bit(1), Bit(1))

        assert vars(metrics) == {
            "bit_instances": 3,
            "nand_calls": 1,
        }


def test_count_metric_without_collection():
    @count_metric("nand_calls")
    def identity() -> str:
        return "done"

    assert identity() == "done"


def test_collect_metrics_restores_previous_context():
    with collect_metrics() as outer:
        Bit(0)

        with collect_metrics() as inner:
            Bit(1)

        Bit(0)

    assert outer.bit_instances == 2
    assert inner.bit_instances == 1
