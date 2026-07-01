import argparse
import os


# from parser import parse_csv
# from extractor import extract_leads
# from writer import write_output

def main():
    perser = argparse.ArgumentParser(description="Regain AI — Lead extraction from CSV using Claude API ")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output", default="output.json", help="Path to output JSON file")
    parser.add_argument("--verbose", action="store_true", help="Print details for each row")
    parser.add_argument("--dry-run", action="store_true", help="Parse CSV only, skip API calls")

    args= parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found — {args.input}")
        exit(1)

    print(f"Starting Regain AI...")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print("File found. Parser, extractor, and writer coming next.")



    if __name__ == "__main__":
        main()