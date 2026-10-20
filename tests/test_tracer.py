import pytest

from src.observability.models import PipelineTrace, SpanStatus
from src.observability.tracer import trace_step


def test_successful_step_is_marked_ok():
    trace = PipelineTrace()

    with trace_step(trace, "extract_jobs"):
        pass

    span = trace.spans[0]
    assert span.status == SpanStatus.OK
    assert span.error is None
    assert span.ended_at is not None
    assert span.ended_at >= span.started_at


def test_failed_step_records_the_exception():
    trace = PipelineTrace()

    with pytest.raises(ValueError):
        with trace_step(trace, "extract_jobs"):
            raise ValueError("Himalayas API is down")

    span = trace.spans[0]
    assert span.status == SpanStatus.FAILED
    assert span.error == "ValueError: Himalayas API is down"
    assert span.ended_at is not None