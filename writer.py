import json  # json.dump for pretty, deterministic output
from datetime import datetime, timezone  # ISO 8601 UTC timestamp for processed_at

from utils import ensure_parent_dir


def write_output(leads, output_path="output.json", success_count=0, error_count=0, dry_run=False, verbose=False):
    """
    Assemble structured lead objects and a metadata block into a single JSON
    document, then write it to output_path.

    Each item in `leads` is expected to already carry its extracted fields
    plus a `source_row` field, as produced by extractor.py. This function
    only formats and writes. It does not validate or transform lead data.

    In dry-run mode the document is built and returned but never written to
    disk, so --dry-run can be verified without touching the filesystem.
    """

    metadata = {
        "total_leads": len(leads),
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "success_count": success_count,
        "error_count": error_count,
    }

    output = {
        "metadata": metadata,
        "leads": leads,
    }

    if dry_run:
        print(f"\n--- Writer Dry Run ---")
        print(f"Leads that would be written: {len(leads)}")
        print(f"Output path (not written):   {output_path}\n")
        return output

    ensure_parent_dir(output_path)

    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(output, outfile, indent=2)

    if verbose:
        print(f"[WRITE] {output_path}")

    print(f"\n--- Writer Summary ---")
    print(f"Leads written: {len(leads)}")
    print(f"Successes:     {success_count}")
    print(f"Errors:        {error_count}")
    print(f"Output file:   {output_path}\n")

    return output
