import csv
from pathlib import Path
from typing import Any, Dict, List

from utils import normalize_phone


REQUIRED_COLUMNS = ["id", "name", "phone", "source"]


def parse_leads_csv(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames:
            raise ValueError("CSV appears to have no header row.")

        missing = [col for col in REQUIRED_COLUMNS if col not in reader.fieldnames]
        if missing:
            raise ValueError(f"CSV missing required columns: {', '.join(missing)}")

        leads: List[Dict[str, Any]] = []
        for row_number, row in enumerate(reader, start=2):
            lead = {key: (value or "").strip() for key, value in row.items()}
            for column in REQUIRED_COLUMNS:
                if not lead.get(column):
                    raise ValueError(
                        f"Row {row_number} is missing required value for '{column}'."
                    )

            lead["phone"] = normalize_phone(lead["phone"])
            leads.append(lead)

        return leads
