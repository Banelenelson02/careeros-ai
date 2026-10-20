
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class SpanStatus(str, Enum):
    RUNNING = "RUNNING"
    OK = "OK"
    FAILED = "FAILED"
    FLAGGED = "FLAGGED"


@dataclass
class Span:
    step_name: str
    trace_id: str
    span_id: str = field(
        default_factory=lambda: str(uuid4())
    )
    status: SpanStatus = SpanStatus.RUNNING
    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    ended_at: datetime | None = None
    error: str | None = None


@dataclass
class PipelineTrace:
    trace_id: str = field(
        default_factory=lambda: str(uuid4())
    )
    spans: list[Span] = field(default_factory=list)
