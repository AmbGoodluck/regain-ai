import argparse
import os
import sys
from typing import Any, Dict, List

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv() -> bool:
        return False

from extractor import extract_lead_insights
from parser import parse_leads_csv
from utils import get_logger, require_env
from writer import write_json_output


LOGGER = get_logger("regain-ai")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse leads from CSV and enrich them with Claude insights."
    )
    parser.add_argument(
        "--input",
        default="sample_leads.csv",
        help="Path to input CSV file (default: sample_leads.csv).",
    )
    parser.add_argument(
        "--output",
        default="leads_output.json",
        help="Path to output JSON file (default: leads_output.json).",
    )
    parser.add_argument(
        "--model",
        default="claude-3-5-sonnet-latest",
        help="Claude model to use (default: claude-3-5-sonnet-latest).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip Claude API calls and output local placeholder insights.",
    )
    return parser


def run(input_path: str, output_path: str, model: str, dry_run: bool) -> int:
    LOGGER.info("Loading leads from %s", input_path)
    leads: List[Dict[str, Any]] = parse_leads_csv(input_path)

    api_key = None
    if not dry_run:
        api_key = require_env("ANTHROPIC_API_KEY")

    enriched: List[Dict[str, Any]] = []
    for lead in leads:
        lead_id = lead.get("id", "unknown")
        LOGGER.info("Processing lead %s", lead_id)
        insights = extract_lead_insights(
            lead=lead,
            model=model,
            api_key=api_key,
            dry_run=dry_run,
        )
        enriched.append({"lead": lead, "insights": insights})

    write_json_output(output_path=output_path, items=enriched)
    LOGGER.info("Done. Wrote %d records to %s", len(enriched), output_path)
    return 0


def main() -> int:
    load_dotenv()
    args = build_parser().parse_args()

    try:
        return run(
            input_path=args.input,
            output_path=args.output,
            model=args.model,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.error("Failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
