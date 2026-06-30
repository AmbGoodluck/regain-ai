# Regain AI

A Python CLI tool that parses website contact form submissions and enriches leads with Claude insights into CRM-ready JSON output.

## Status

In Progress

## Planned Features

- CSV contact form ingestion
- AI-powered data extraction and structuring
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
├── .env.example
├── requirements.txt
├── README.md
├── PRD.md
└── SPEC.md

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
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

Run in dry mode (no API calls):

```bash
python main.py --input sample_leads.csv --output leads_output.json --dry-run
```

Optional model override:

```bash
python main.py --model claude-3-5-sonnet-latest
```

## Output

The tool writes JSON in this shape:

```json
{
	"generated_at": "...",
	"count": 3,
	"results": [
		{
			"lead": {"id": "1", "name": "..."},
			"insights": {
				"summary": "...",
				"urgency": "medium",
				"intent": "...",
				"next_action": "..."
			}
		}
	]
}
```
