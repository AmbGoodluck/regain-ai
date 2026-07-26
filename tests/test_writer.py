import json

from writer import write_output


SAMPLE_LEADS = [
    {"full_name": "Marcus Johnson", "email": "marcus@example.com", "source_row": 1, "needs_review": False},
    {"full_name": "Dana Lee", "email": "dana@example.com", "source_row": 2, "needs_review": True},
]


def test_write_output_writes_valid_json_file(tmp_path):
    output_path = tmp_path / "output.json"

    write_output(SAMPLE_LEADS, output_path=str(output_path), success_count=2, error_count=0)

    assert output_path.exists()
    with open(output_path, encoding="utf-8") as f:
        data = json.load(f)

    assert data["leads"] == SAMPLE_LEADS
    assert data["metadata"]["total_leads"] == 2
    assert data["metadata"]["success_count"] == 2
    assert data["metadata"]["error_count"] == 0
    assert "processed_at" in data["metadata"]


def test_write_output_dry_run_does_not_touch_disk(tmp_path):
    output_path = tmp_path / "output.json"

    result = write_output(SAMPLE_LEADS, output_path=str(output_path), dry_run=True)

    assert not output_path.exists()
    assert result["metadata"]["total_leads"] == 2
    assert result["leads"] == SAMPLE_LEADS


def test_write_output_creates_parent_directories(tmp_path):
    output_path = tmp_path / "nested" / "dir" / "output.json"

    write_output([], output_path=str(output_path))

    assert output_path.exists()


def test_write_output_handles_empty_leads_list(tmp_path):
    output_path = tmp_path / "output.json"

    data = write_output([], output_path=str(output_path))

    assert data["metadata"]["total_leads"] == 0
    assert data["leads"] == []
