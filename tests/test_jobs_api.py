import pytest
import requests

from src.extract import jobs_api
from src.observability.models import PipelineTrace, SpanStatus

GOOD_JOB = {
    "title": "Data Engineer",
    "companyName": "Example Co",
    "applicationLink": "https://example.com/apply",
    "guid": "abc-123",
}


def test_failed_request_is_traced(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.ConnectionError("no internet")

    monkeypatch.setattr(jobs_api.requests, "get", fake_get)
    trace = PipelineTrace()

    with pytest.raises(requests.ConnectionError):
        jobs_api.run_extraction(trace)

    assert len(trace.spans) == 1
    assert trace.spans[0].step_name == "fetch_jobs"
    assert trace.spans[0].status == SpanStatus.FAILED
    assert "ConnectionError" in trace.spans[0].error


def test_successful_extraction_is_traced(monkeypatch, tmp_path):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"jobs": [GOOD_JOB]}

    monkeypatch.setattr(jobs_api.requests, "get", lambda *a, **k: FakeResponse())
    monkeypatch.setattr(
        jobs_api, "save_bronze", lambda data: tmp_path / "jobs.json"
    )
    trace = PipelineTrace()

    data, _ = jobs_api.run_extraction(trace)

    assert [s.step_name for s in trace.spans] == [
        "fetch_jobs",
        "save_bronze",
        "validate_jobs",
    ]
    assert all(s.status == SpanStatus.OK for s in trace.spans)


def test_empty_result_is_flagged_not_failed(monkeypatch, tmp_path):
    class EmptyResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"jobs": []}

    monkeypatch.setattr(jobs_api.requests, "get", lambda *a, **k: EmptyResponse())
    monkeypatch.setattr(
        jobs_api, "save_bronze", lambda data: tmp_path / "jobs.json"
    )
    trace = PipelineTrace()

    jobs_api.run_extraction(trace)  # must NOT raise

    last = trace.spans[-1]
    assert last.step_name == "validate_jobs"
    assert last.status == SpanStatus.FLAGGED
    assert last.error == "No jobs returned"