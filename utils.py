"""Shared utilities for the Regain AI CLI workflow."""

import os
from typing import Any, Mapping, Optional


def normalize_scalar(value: Any) -> str:
    """Return a trimmed string representation of the provided value."""
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    return str(value).strip()


def is_blank(value: Any) -> bool:
    """Return True when the provided value is empty or whitespace-only."""
    return normalize_scalar(value) == ""


def normalize_row(row: Optional[Mapping[str, Any]]) -> dict[str, str]:
    """Return a cleaned copy of a mapping with trimmed keys and values."""
    if not row:
        return {}

    return {
        normalize_scalar(key): normalize_scalar(value)
        for key, value in row.items()
    }


def get_field(row: Optional[Mapping[str, Any]], key: str, default: Any = "") -> str:
    """Safely read a normalized field from a mapping."""
    if row is None:
        return normalize_scalar(default)

    return normalize_scalar(row.get(key, default))


def ensure_parent_dir(path: str) -> None:
    """Create the parent directory for a file path when it does not exist."""
    parent = os.path.dirname(os.path.abspath(path))

    if parent:
        os.makedirs(parent, exist_ok=True)
