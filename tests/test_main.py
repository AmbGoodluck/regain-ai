import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_CSV = REPO_ROOT / "sample_leads.csv"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "main.py"), *args],
        capture_output=True,
        text=True,
    )


def test_missing_input_file_exits_with_error():
    result = run_cli("--input", "does_not_exist.csv")

    assert result.returncode == 1
    assert "File not found" in result.stdout


def test_dry_run_parses_sample_csv_without_writing_output(tmp_path):
    output_path = tmp_path / "output.json"

    result = run_cli("--input", str(SAMPLE_CSV), "--output", str(output_path), "--dry-run")

    assert result.returncode == 0
    assert "CSV Parse Summary" in result.stdout
    assert "Writer Dry Run" in result.stdout
    assert not output_path.exists()


def test_dry_run_on_empty_csv_exits_cleanly(tmp_path):
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("name,email\n", encoding="utf-8")

    result = run_cli("--input", str(empty_csv), "--dry-run")

    assert result.returncode == 0
    assert "No rows to process" in result.stdout


def test_full_flow_with_mocked_extractor_writes_output_json(tmp_path, monkeypatch):
    """
    End-to-end run of the real CLI pipeline (parse -> extract -> write) with
    only the Claude API call swapped for a stub, so the wiring in main.py is
    verified without needing a real ANTHROPIC_API_KEY or network access.
    """
    output_path = tmp_path / "output.json"

    def fake_extract_leads(rows, verbose=False):
        leads = [
            {**row, "full_name": row.get("name", ""), "source_row": i, "needs_review": False}
            for i, row in enumerate(rows, start=1)
        ]
        return leads, len(leads), 0

    import main as main_module

    monkeypatch.setattr(main_module, "extract_leads", fake_extract_leads)
    monkeypatch.setattr(
        sys, "argv", ["main.py", "--input", str(SAMPLE_CSV), "--output", str(output_path)]
    )

    main_module.main()

    assert output_path.exists()
    with open(output_path, encoding="utf-8") as f:
        data = json.load(f)

    assert data["metadata"]["total_leads"] == 3
    assert data["metadata"]["success_count"] == 3
    assert data["metadata"]["error_count"] == 0
    assert len(data["leads"]) == 3
