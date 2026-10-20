from contextlib import contextmanager
from datetime import datetime, timezone

from src.observability.models import PipelineTrace, Span, SpanStatus


@contextmanager
def trace_step(trace: PipelineTrace, step_name: str):
    """Record one pipeline step as a Span inside the given trace."""
    span = Span(step_name=step_name, trace_id=trace.trace_id)
    trace.spans.append(span)

    try:
        yield span
        if span.status == SpanStatus.RUNNING:  # the step didn't set its own status
            span.status = SpanStatus.OK
    except Exception as exc:
        span.status = SpanStatus.FAILED
        span.error = f"{type(exc).__name__}: {exc}"
        raise  # we record the failure, we don't hide it
    finally:
        span.ended_at = datetime.now(timezone.utc)