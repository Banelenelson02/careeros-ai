
import requests
from src.extract.bronze_writer import save_bronze

url = "https://himalayas.app/jobs/api"

response = requests.get(
    url,
    params={"limit": 5},
    timeout=15
)

response.raise_for_status()

# First: Convert the JSON response into Python data
data = response.json()

# Second: Save the data to the Bronze layer
file_path = save_bronze(data)

print("Bronze data saved to:", file_path)

# Third: Inspect the extracted jobs
jobs = data.get("jobs", [])

print("Jobs received:", len(jobs))

if jobs:
    first_job = jobs[0]

    print("\nAvailable fields:")

    for field, value in first_job.items():
        print(
            field,
            "->",
            type(value).__name__
        )
