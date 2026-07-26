from utils import ensure_parent_dir, get_field, is_blank, normalize_row, normalize_scalar


def test_normalize_scalar_strips_whitespace():
    assert normalize_scalar("  hello  ") == "hello"


def test_normalize_scalar_handles_none():
    assert normalize_scalar(None) == ""


def test_normalize_scalar_stringifies_non_string_values():
    assert normalize_scalar(42) == "42"


def test_is_blank_true_for_empty_and_whitespace():
    assert is_blank("") is True
    assert is_blank("   ") is True
    assert is_blank(None) is True


def test_is_blank_false_for_content():
    assert is_blank("hi") is False


def test_normalize_row_trims_keys_and_values():
    row = {" Name ": " Dana ", "email ": " dana@example.com "}
    assert normalize_row(row) == {"Name": "Dana", "email": "dana@example.com"}


def test_normalize_row_handles_empty_input():
    assert normalize_row(None) == {}
    assert normalize_row({}) == {}


def test_get_field_returns_normalized_value():
    row = {"phone": "  415-555-0101  "}
    assert get_field(row, "phone") == "415-555-0101"


def test_get_field_returns_default_when_missing():
    assert get_field({}, "phone", default="unknown") == "unknown"


def test_get_field_handles_none_row():
    assert get_field(None, "phone", default="n/a") == "n/a"


def test_ensure_parent_dir_creates_missing_directory(tmp_path):
    target = tmp_path / "nested" / "dir" / "file.json"
    assert not target.parent.exists()

    ensure_parent_dir(str(target))

    assert target.parent.exists()


def test_ensure_parent_dir_noop_for_existing_directory(tmp_path):
    target = tmp_path / "file.json"

    ensure_parent_dir(str(target))  # should not raise even though tmp_path already exists
