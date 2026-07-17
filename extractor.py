import json  # build/parse the structured request and response
import os  # read ANTHROPIC_API_KEY from the environment
import re  # lightweight email/phone validation for needs_review
import time  # backoff sleep between rate-limited retries

from anthropic import Anthropic, APIError, RateLimitError
from dotenv import load_dotenv  # loads ANTHROPIC_API_KEY from a local .env file

MODEL = "claude-sonnet-4-6"
MAX_RATE_LIMIT_RETRIES = 3  # F5: exponential backoff, max 3 retries on rate limit

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _build_client():
    load_dotenv()
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Missing ANTHROPIC_API_KEY. Copy .env.example to .env and add your key."
        )

    return Anthropic(api_key=api_key)


def _build_prompt(row):
    # temperature=0 plus an explicit schema keeps output deterministic across identical rows
    row_json = json.dumps(row)
    return f"""You are extracting structured lead data from one contact form submission.

Row data (JSON): {row_json}

Return ONLY a single JSON object with exactly these keys, no markdown fences and no extra text:
- "full_name": string
- "email": string
- "phone": string
- "service_requested": string, inferred from the notes/message field
- "urgency": one of "high", "medium", "low"
- "preferred_contact_time": string, or "" if not mentioned

If a field is missing from the row, infer it from context when possible, otherwise use an empty string."""


def _parse_json_response(text):
    # Claude is instructed to return raw JSON, but slicing between the outer
    # braces tolerates the occasional stray markdown fence or commentary.
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found in Claude response")

    return json.loads(text[start:end + 1])


def _needs_review(email, phone):
    email_ok = bool(EMAIL_RE.match(email)) if email else False
    phone_digits = re.sub(r"\D", "", phone) if phone else ""
    phone_ok = 7 <= len(phone_digits) <= 15
    return not (email_ok and phone_ok)


def _call_claude(client, row, verbose=False):
    """Send one row to Claude and return the parsed extraction dict, retrying on failure."""
    prompt = _build_prompt(row)

    rate_limit_attempts = 0
    generic_retry_used = False
    delay = 1

    while True:
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=300,
                temperature=0,
                messages=[{"role": "user", "content": prompt}],
            )
            return _parse_json_response(response.content[0].text)

        except RateLimitError:
            rate_limit_attempts += 1
            if rate_limit_attempts > MAX_RATE_LIMIT_RETRIES:
                raise
            if verbose:
                print(f"[RETRY] rate limited, waiting {delay}s "
                      f"(attempt {rate_limit_attempts}/{MAX_RATE_LIMIT_RETRIES})")
            time.sleep(delay)
            delay *= 2

        except (APIError, ValueError, json.JSONDecodeError) as error:
            # F2: non-rate-limit errors get a single retry, then the row is logged and skipped
            if generic_retry_used:
                raise
            generic_retry_used = True
            if verbose:
                print(f"[RETRY] {error}")


def extract_leads(rows, verbose=False):
    """
    Send each parsed CSV row to the Claude API for structured extraction.

    Returns (leads, success_count, error_count). Each lead dict carries the
    extracted fields plus source_row for traceability and needs_review when
    the email or phone looks malformed. A row that still fails after retries
    is logged and skipped rather than aborting the whole run.
    """
    client = _build_client()

    leads = []
    success_count = 0
    error_count = 0

    for source_row, row in enumerate(rows, start=1):
        try:
            extracted = _call_claude(client, row, verbose=verbose)
        except Exception as error:
            error_count += 1
            print(f"[ERROR] row {source_row}: {error}")
            continue

        extracted["source_row"] = source_row
        extracted["needs_review"] = _needs_review(extracted.get("email", ""), extracted.get("phone", ""))

        if verbose:
            print(f"[EXTRACTED] {extracted}")

        leads.append(extracted)
        success_count += 1

    print(f"\n--- Extractor Summary ---")
    print(f"Leads extracted: {success_count}")
    print(f"Rows failed:     {error_count}")
    print(f"Total rows:      {success_count + error_count}\n")

    return leads, success_count, error_count
