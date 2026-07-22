"""Shared utilities for the Regain AI CLI workflow."""

import os  # directory creation for output paths


def normalize_scalar(value):
    """Return a trimmed string representation of value, or an empty string."""
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    return str(value).strip()


def is_blank(value):
    """Return True when a value is empty or only whitespace."""
    return normalize_scalar(value) == ""


def normalize_row(row):
    """Return a cleaned copy of a mapping with trimmed keys and values."""
    if not row:
        return {}

    return {
        normalize_scalar(key): normalize_scalar(value)
        for key, value in row.items()
    }


def get_field(row, key, default=""):
    """Safely read a normalized field from a mapping, falling back cleanly."""
    if row is None:
        return normalize_scalar(default)

    return normalize_scalar(row.get(key, default))


def ensure_parent_dir(path):
    """Create the parent directory for a file path when it does not exist."""
    parent = os.path.dirname(os.path.abspath(path))

    if parent:
        os.makedirs(parent, exist_ok=True)
