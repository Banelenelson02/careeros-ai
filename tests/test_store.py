import pytest
import psycopg

from src.database.connection import get_connection
from src.observability.models import PipelineTrace
from src.observability.store import ensure_tables, save_trace
from src.observability.tracer import trace_step


@pytest.fixture
def connection():
    try:
        conn = get_connection()
    except psycopg.OperationalError:
        pytest.skip("Postgres is not running (try: docker compose up -d)")
    ensure_tables(conn)
    yield conn
    conn.close()


def test_trace_is_saved_to_postgres(connection):
    trace = PipelineTrace()

    with trace_step(trace, "fetch_jobs"):
        pass
    with pytest.raises(ValueError):
        with trace_step(trace, "save_bronze"):
            raise ValueError("disk full")

    assert save_trace(connection, trace) == 2

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT step_name, status, error FROM pipeline_spans "
            "WHERE trace_id = %s ORDER BY started_at",
            (trace.trace_id,),
        )
        rows = cursor.fetchall()

    assert rows == [
        ("fetch_jobs", "OK", None),
        ("save_bronze", "FAILED", "ValueError: disk full"),
    ]

    # clean up so test runs don't pile up rows
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM pipeline_spans WHERE trace_id = %s", (trace.trace_id,)
        )
    connection.commit()