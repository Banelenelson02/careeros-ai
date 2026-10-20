REQUIRED_FIELDS = ("title", "companyName", "applicationLink", "guid")


def check_jobs(data: dict) -> str | None:
    """Return a description of the problem, or None if the data looks fine."""
    jobs = data.get("jobs", [])

    if not jobs:
        return "No jobs returned"

    broken = [
        job for job in jobs
        if any(not job.get(field) for field in REQUIRED_FIELDS)
    ]
    if broken:
        return f"{len(broken)} of {len(jobs)} jobs are missing a required field"

    return None