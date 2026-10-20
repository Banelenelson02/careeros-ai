from src.extract.validation import check_jobs

GOOD_JOB = {
    "title": "Junior Data Engineer",
    "companyName": "Example Co",
    "applicationLink": "https://example.com/apply",
    "guid": "abc-123",
}


def test_good_data_has_no_problem():
    assert check_jobs({"jobs": [GOOD_JOB]}) is None


def test_empty_jobs_is_a_problem():
    assert check_jobs({"jobs": []}) == "No jobs returned"


def test_missing_field_is_a_problem():
    bad_job = {**GOOD_JOB, "companyName": None}
    result = check_jobs({"jobs": [GOOD_JOB, bad_job]})
    assert result == "1 of 2 jobs are missing a required field"