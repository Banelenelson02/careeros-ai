from psycopg import Connection

from src.observability.models import PipelineTrace

CREATE_SPANS_TABLE = """
CREATE TABLE IF NOT EXISTS pipeline_spans (
    span_id     TEXT PRIMARY KEY,
    trace_id    TEXT NOT NULL,
    step_name   TEXT NOT NULL,
    status      TEXT NOT NULL,
    started_at  TIMESTAMPTZ NOT NULL,
    ended_at    TIMESTAMPTZ,
    error       TEXT
);
"""

INSERT_SPAN = """
INSERT INTO pipeline_spans
    (span_id, trace_id, step_name, status, started_at, ended_at, error)
VALUES
    (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (span_id) DO NOTHING;
"""


def ensure_tables(connection: Connection) -> None:
    """Create the pipeline_spans table if it doesn't exist yet."""
    with connection.cursor() as cursor:
        cursor.execute(CREATE_SPANS_TABLE)
    connection.commit()


def save_trace(connection: Connection, trace: PipelineTrace) -> int:
    """Save every span in the trace. Returns how many spans were given."""
    with connection.cursor() as cursor:
        for span in trace.spans:
            cursor.execute(
                INSERT_SPAN,
                (
                    span.span_id,
                    span.trace_id,
                    span.step_name,
                    span.status.value,
                    span.started_at,
                    span.ended_at,
                    span.error,
                ),
            )
    connection.commit()
    return len(trace.spans)