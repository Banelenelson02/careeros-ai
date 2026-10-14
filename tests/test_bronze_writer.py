import json

from src.extract.bronze_writer import save_bronze

def test_save_bronze_creates_file(tmp_path):
    sample_data = {
        "jobs": [
            {
                "title": "Junior Data Engineer",
                "CompanyName" : "Example Company",
                "minSalary" :None
            }
        ]
    }

    file_path = save_bronze(sample_data, directory=tmp_path)
    assert file_path.exists()