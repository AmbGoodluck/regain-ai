import csv  # DictReader for row-as-dict parsing
import os   # file existence check before open


def parse_csv(filepath, verbose=False):
    """
    Read a CSV file and return a list of cleaned row dictionaries.
    Skips empty rows. Strips whitespace from all keys and values.
    """

    rows = []
    skipped = 0

    with open(filepath, encoding="utf-8-sig") as csvfile:

        reader = csv.DictReader(csvfile)  # each row becomes {header: value}

        for row in reader:

            # strip whitespace from every key and value in the row
            cleaned_row = {key.strip(): value.strip() for key, value in row.items()}

            # skip rows where every field is blank
            if all(value == "" for value in cleaned_row.values()):
                skipped += 1
                if verbose:
                    print("[SKIP] empty row")
                continue

            if verbose:
                print(f"[READ] {cleaned_row}")

            rows.append(cleaned_row)

    print(f"\n--- CSV Parse Summary ---")
    print(f"Rows parsed:  {len(rows)}")
    print(f"Rows skipped: {skipped}")
    print(f"Total rows:   {len(rows) + skipped}\n")

    return rows