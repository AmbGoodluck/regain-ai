# Regain AI - Product Requirements Document
Portfolio Project: CLI Phase

| Field | Detail |
|---|---|
| Version | 2.0 (Portfolio Rebuild) |
| Owner | Osman Amadu Jalloh |
| Status | Active Build |
| Last Updated | June 2026 |
| GitHub Repo | github.com/AmbGoodluck/regain-ai |
| Primary Goal | Demonstrate Python + Claude API proficiency to 2027 internship recruiters |


## 1. One-Line Summary

Regain AI is a Python CLI tool that reads a CSV of contact form submissions on websites, uses the Claude API to extract and structure lead data, and outputs a CRM-ready JSON file, demonstrating real-world AI integration, data processing, and clean software engineering.

---

## 2. Context & Purpose

### Why This Project Exists

This project was scoped specifically to serve as a portfolio centerpiece for Summer 2027 tech internship recruiting. It is not a consumer product at this stage. The original Regain AI vision (an AI-powered voice callback system for home services contractors) remains the long-term direction. This CLI tool is Phase 1: a real, shippable artifact that demonstrates the core competency (AI-driven data transformation) without requiring infrastructure that is out of scope for the current skill level and timeline.

### The Problem It Solves

Service businesses receive contact form submissions and frequently lose leads to slow or disorganized follow-up. The data that arrives is messy, inconsistent, and not CRM-ready. A tool that ingests raw CSV submissions, extracts structured lead intelligence using AI, and outputs a clean JSON file creates immediate, demonstrable value while showcasing Python and API integration skills.

---

## 3. Goals

### Portfolio Goals

- Demonstrate practical Python proficiency: file I/O, CSV parsing, JSON output, API calls
- Demonstrate AI integration: real use of the Claude API with structured prompting
- Produce a README and and this PRD to documentation clear enough that a recruiter understands the project in 60 seconds

### Product Goals (Phase 1)

- Correctly parse a CSV of contact form submissions with varying column structures
- Extract structured fields per lead: name, email, phone, service requested, urgency, preferred contact time
- Output a valid, well-formatted JSON file importable into standard CRM tools
- Handle edge cases gracefully: missing fields, malformed rows, empty submissions


## 4. Non-Goals (Phase 1)

The following are explicitly out of scope for the current build. Including them would delay shipping and dilute focus.

- No web interface, dashboard, or UI of any kind
- No automated calling, voice cloning, or Vapi/Retell integration
- No calendar booking or Cal.com connection
- No database, Supabase, or persistent storage
- No real-time webhook processing or live lead capture
- No paid subscription model or billing
- No multi-user or team functionality

*These features belong to Phase 2 (full SaaS build), which begins after first paying customers are acquired.

---

## 5. Target User (Phase 1)

The Phase 1 user is a recruiter or hiring manager evaluating the GitHub repo or anyother friend i ask to help evaluate, not an end customer.
Secondary user: myself (Osman), validating that the tool works correctly on real or synthetic CSV data.

| Attribute | Detail |
|---|---|
| Who | Recruiter at any of the companies i apply to. 
| What they see | A GitHub repo with real commits, clean Python, Claude API usage, and a clear README |
| What convinces them | Consistent commit history, working code, documented output, and a genuine use case |

---

## 6. Feature Requirements

### F1: CSV Ingestion

- Accept a file path to a CSV as a CLI argument
- Parse all rows, handling quoted fields and missing columns without crashing
- Log a summary of rows parsed, rows skipped, and errors encountered
- Support common contact form column names: name, email, phone, message, date, service

### F2: AI Extraction via Claude API

- Send each row's raw data to the Claude API with a structured extraction prompt
- Extract: full name, email address, phone number, service type requested, urgency level (high/medium/low), preferred contact time
- Return extraction as structured JSON per lead
- Handle API errors gracefully: retry once, then log failure and continue to next row
- Prompt must be deterministic and produce consistent output across identical inputs

### F3: JSON Output

- Write a single `output.json` file containing an array of structured lead objects
- Each object includes all extracted fields plus a `source_row` field for traceability
- Include a metadata block: `total_leads`, `processed_at` timestamp, `success_count`, `error_count`
- Output path configurable via CLI flag (default: `./output.json`)

### F4: CLI Interface

- Entry point: `python main.py --input leads.csv`
- Optional flags: `--output` (path), `--verbose` (show per-row processing), `--dry-run` (parse without calling API)
- Clear success/error messages printed to stdout
- Exit code 0 on success, 1 on fatal error

### F5: Error Handling & Edge Cases

- Empty CSV: exit gracefully with a meaningful message
- Missing required columns: skip row, log warning, continue
- Malformed email or phone: include field as-is, flag as `needs_review: true` in output
- API rate limit hit: implement exponential backoff with max 3 retries
- Missing API key: clear error message directing to `.env` setup

---

## 7. Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Language | Python 3.11+ | CS50P curriculum alignment; recruiter-friendly |
| AI | Claude API (claude-sonnet-4-6) | Real API integration; demonstrates AI tooling |
| CSV Parsing | Python `csv` module (stdlib) | No extra dependencies; shows stdlib knowledge |
| JSON Output | Python `json` module (stdlib) | Clean, standard output format |
| Env Management | python-dotenv | Keeps API key out of source code |
| CLI Args | argparse (stdlib) | Clean CLI without heavy frameworks |
| Version Control | Git + GitHub | Public repo for recruiter visibility |

---

## 8. Repo Structure

```
regain-ai/
├── main.py              # CLI entry point
├── parser.py            # CSV ingestion logic
├── extractor.py         # Claude API calls & prompt
├── writer.py            # JSON output formatting
├── utils.py             # Shared helpers (logging, validation)
├── sample_leads.csv     # Sample input for testing
├── .env.example         # API key template (no real key committed)
├── requirements.txt     # Dependencies
└── README.md            # Project overview + usage instructions
```


## 9. Release Plan

| Milestone | Target | Deliverables |
|---|---|---|
| M0: Setup | Week 1 | GitHub repo created, README written, folder structure committed, first commit live |
| M1: Parser | Week 2 | `main.py` CLI entry point, `parser.py` reads CSV, logs row count and errors, handles missing columns |
| M2: Extractor | Week 3 | `extractor.py` built, structured prompt written, returns clean JSON per row, error + retry handling |
| M3: Writer | Week 3–4 | `writer.py` formats output, metadata block included, `output.json` written to disk, dry-run flag working |
| M4: v1.0 | Mid-July | End-to-end test on sample CSV, README updated with usage + example output, `requirements.txt` finalized, repo public and clean |

---

## 10. Success Criteria

This project is complete when all of the following are true:

- Running `python main.py --input sample_leads.csv` produces a valid `output.json` with no unhandled exceptions
- The GitHub repo has at least 15 commits spanning more than 2 weeks, showing genuine incremental development
- The README explains what the tool does, how to run it, and shows example input/output in under 60 seconds of reading
- A recruiter who clicks the repo can understand the project, the tech stack, and the candidate's skill level without asking a question
- The code is clean: no dead code, no hardcoded API keys, no print-statement debugging left in production

---

## 11. Phase 2: Future Vision

Phase 2 converts this CLI tool into the full Regain AI SaaS product: a web application that monitors live contact form submissions via webhooks, triggers AI-powered voice callbacks within 60 seconds using Vapi or Retell, books appointments via Cal.com, and tracks recovered revenue in a Supabase-backed leads ledger.

Phase 2 begins only after Phase 1 is shipped, CS50P is complete, and at least one 2027 internship application has been submitted. It is not in scope for Summer 2026.
