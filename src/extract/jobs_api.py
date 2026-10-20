import requests

from src.extract.bronze_writer import save_bronze
from src.observability.models import PipelineTrace
from src.observability.tracer import trace_step

URL = "https://himalayas.app/jobs/api"


def run_extraction(trace: PipelineTrace, url: str = URL, limit: int = 5):
    """Fetch jobs from Himalayas and save them to Bronze, tracing each step."""
    with trace_step(trace, "fetch_jobs"):
        response = requests.get(url, params={"limit": limit}, timeout=15)
        response.raise_for_status()
        data = response.json()

    with trace_step(trace, "save_bronze"):
        file_path = save_bronze(data)

    return data, file_path


def print_trace(trace: PipelineTrace) -> None:
    print(f"\nTrace {trace.trace_id}")
    for span in trace.spans:
        seconds = (span.ended_at - span.started_at).total_seconds()
        line = f"  {span.step_name:<12} {span.status.value:<8} {seconds:.3f}s"
        if span.error:
            line += f"  <- {span.error}"
        print(line)


if __name__ == "__main__":
    trace = PipelineTrace()
    try:
        data, file_path = run_extraction(trace)
        print("Bronze data saved to:", file_path)
        print("Jobs received:", len(data.get("jobs", [])))
    finally:
        print_trace(trace)  # prints even when a step failed