# Regain AI

[![Tests](https://github.com/AmbGoodluck/regain-ai/actions/workflows/tests.yml/badge.svg)](https://github.com/AmbGoodluck/regain-ai/actions/workflows/tests.yml)

I built this Python CLI to take a CSV of website contact form submissions, send each row to the Claude API for structured extraction, and write the results to a CRM-ready JSON file. It's Phase 1 of a larger idea (see `PRD.md`) — a standalone, working tool rather than a demo stub.

## Status

The CLI runs end to end: CSV in, Claude extraction, JSON out. Covered by a pytest suite (unit tests plus a full CLI run).

## Features

- CSV contact form ingestion, with blank rows skipped and a parse summary logged
- Structured lead extraction via the Claude API (name, email, phone, service requested, urgency, preferred contact time)
- Retry handling for rate limits (exponential backoff) and transient API errors
- JSON output with a metadata block (`total_leads`, `processed_at`, `success_count`, `error_count`)
- `--dry-run` to parse and preview without calling the API or touching disk

Phase 2 (not part of this CLI) is the full SaaS direction from `PRD.md`/`SPEC.md`: a webhook-driven ledger that triggers AI voice callbacks and books appointments via Cal.com.

## Tech Stack

- Python (stdlib `csv`, `json`, `argparse`)
- Claude API (`anthropic` SDK)
- pytest for testing

## Project Structure

.
├── main.py
├── parser.py
├── extractor.py
├── writer.py
├── utils.py
├── sample_leads.csv
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── README.md
├── PRD.md
└── SPEC.md

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

   To also run the test suite, install `requirements-dev.txt` instead — it pulls in the runtime dependencies above plus pytest:

   ```bash
   pip install -r requirements-dev.txt
   ```

3. Create a local environment file from the template:

```bash
cp .env.example .env
```

4. Add your real Anthropic key to `.env`:

```dotenv
ANTHROPIC_API_KEY=your_real_key_here
```

## Usage

Run with live Claude API calls:

```bash
python main.py --input sample_leads.csv --output leads_output.json
```

Run in dry mode (parses the CSV and previews the write, but skips the Claude API and never touches disk):

```bash
python main.py --input sample_leads.csv --output leads_output.json --dry-run
```

Add `--verbose` to print per-row detail: parsing on every run, plus Claude extraction detail on a live run.

## Output

The tool writes JSON in this shape (`processed_at` is generated at write time — the value below is just an example):

```json
{
  "metadata": {
    "total_leads": 3,
    "processed_at": "2026-07-25T18:04:00+00:00",
    "success_count": 3,
    "error_count": 0
  },
  "leads": [
    {
      "full_name": "Marcus Johnson",
      "email": "marcus@example.com",
      "phone": "(415) 555-0101",
      "service_requested": "roof repair",
      "urgency": "high",
      "preferred_contact_time": "",
      "source_row": 1,
      "needs_review": false
    }
  ]
}
```

## Testing

The test suite covers CSV parsing, JSON writing, the Claude extraction logic (mocked — no API key or network access required), and an end-to-end run of the CLI itself.

```bash
pip install -r requirements-dev.txt
pytest -v
```

To manually verify the full flow end-to-end:

```bash
# 1. Dry run — confirms parsing works, no API key needed
python main.py --input sample_leads.csv --dry-run --verbose

# 2. Live run — enriches sample_leads.csv with Claude and writes leads_output.json
python main.py --input sample_leads.csv --output leads_output.json --verbose
cat leads_output.json
```
