from parser import parse_csv


def write_csv(tmp_path, content):
    path = tmp_path / "leads.csv"
    path.write_text(content, encoding="utf-8")
    return str(path)


def test_parse_csv_strips_whitespace_from_keys_and_values(tmp_path):
    csv_path = write_csv(
        tmp_path,
        "name , email\n Dana Lee , dana@example.com \n",
    )

    rows = parse_csv(csv_path)

    assert rows == [{"name": "Dana Lee", "email": "dana@example.com"}]


def test_parse_csv_skips_fully_blank_rows(tmp_path):
    csv_path = write_csv(
        tmp_path,
        "name,email\nMarcus,marcus@example.com\n,\nDana,dana@example.com\n",
    )

    rows = parse_csv(csv_path)

    assert len(rows) == 2
    assert rows[0]["name"] == "Marcus"
    assert rows[1]["name"] == "Dana"


def test_parse_csv_returns_empty_list_for_header_only_file(tmp_path):
    csv_path = write_csv(tmp_path, "name,email\n")

    rows = parse_csv(csv_path)

    assert rows == []


def test_parse_csv_returns_empty_list_for_empty_file(tmp_path):
    csv_path = write_csv(tmp_path, "")

    rows = parse_csv(csv_path)

    assert rows == []


def test_parse_csv_handles_utf8_bom(tmp_path):
    path = tmp_path / "leads.csv"
    path.write_bytes("name,email\nPriya,priya@example.com\n".encode("utf-8-sig"))

    rows = parse_csv(str(path))

    assert rows == [{"name": "Priya", "email": "priya@example.com"}]


def test_parse_csv_verbose_prints_summary(tmp_path, capsys):
    csv_path = write_csv(tmp_path, "name,email\nMarcus,marcus@example.com\n")

    parse_csv(csv_path, verbose=True)

    captured = capsys.readouterr()
    assert "[READ]" in captured.out
    assert "CSV Parse Summary" in captured.out
