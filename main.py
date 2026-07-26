import argparse
import os

from parser import parse_csv
from extractor import extract_leads
from writer import write_output


def main():
    parser = argparse.ArgumentParser(description="Regain AI — Lead extraction from CSV using Claude API")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output", default="output.json", help="Path to output JSON file")
    parser.add_argument("--verbose", action="store_true", help="Print details for each row")
    parser.add_argument("--dry-run", action="store_true", help="Parse CSV only, skip API calls")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found — {args.input}")
        raise SystemExit(1)

    print("Starting Regain AI...")
    print(f"Input:  {args.input}")
    print(f"Output: {args.output}")

    rows = parse_csv(args.input, verbose=args.verbose)

    if not rows:
        print("No rows to process. Exiting.")
        return

    if args.dry_run:
        write_output([], output_path=args.output, dry_run=True, verbose=args.verbose)
        return

    try:
        leads, success_count, error_count = extract_leads(rows, verbose=args.verbose)
    except RuntimeError as error:
        print(f"Error: {error}")
        raise SystemExit(1)

    write_output(
        leads,
        output_path=args.output,
        success_count=success_count,
        error_count=error_count,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
