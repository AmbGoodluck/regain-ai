import os

import csv

def parse_csv(filepath, verbose-False):
    
    row = []
    skipped = 0

    with open(filepath, encoding="utf-8-sig") as cvsfile:

        reader = csv.DictReader(csvfile)

        for row in reader:
            cleaned_row = {key.strip(): value.strip() for key, value in row.items()} 

            skipped += 1

            if verbose:
                print(f"Skipped empty row")

            continue



            # Add the cleaned row to our rows list
            rows.append(cleaned_row)

    # After the loop, print a summary of what we found
    print(f"\nCSV Parsing Complete")
    print(f"Rows read:    {len(rows)}")
    print(f"Rows skipped: {skipped}")
    print(f"Total:        {len(rows) + skipped}\n")

    # Return the list of rows so main.py can use it
    return rows


