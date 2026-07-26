# Regain AI

A Python CLI tool that parses website contact form submissions and enriches leads with Claude insights into CRM-ready JSON output.

## Status

Working — v1.0

## Features

- CSV contact form ingestion
- AI-powered data extraction and structuring via the Claude API
- JSON output formatted for CRM import
- (Phase 2) Automated follow-up via Twilio

## Tech Stack

- Python
- Claude API
- CSV / JSON

CLI tool for ingesting lead data from CSV, enriching each lead with Claude-generated insights, and exporting results to JSON.

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

For running the test suite, install the dev dependencies instead (this also installs the runtime dependencies above):

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

Add `--verbose` to either command to print per-row parsing and extraction detail.

## Output

The tool writes JSON in this shape:

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
