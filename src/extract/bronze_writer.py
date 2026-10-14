
import json
from pathlib import Path
from datetime import datetime, timezone


def save_bronze(
    data: dict,
    directory: Path = Path("data/bronze/himalayas")
) -> Path:
    directory = Path("data/bronze/himalayas")
    directory.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    file_path = directory / f"jobs_{timestamp}.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return file_path
