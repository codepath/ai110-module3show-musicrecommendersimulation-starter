from src.main import print_recommendations
from src.recommender import load_songs, recommend_songs
from src.table import render_table

HEADERS = ["#", "Song", "Score", "Reasons"]


def lines_of(table: str):
    return table.split("\n")


def test_every_line_of_the_table_has_the_same_width():
    rows = [("1", "Song A\nby Artist", "3.00/4.00", "- genre match (+1.0)\n- mood match (+1.0)"),
            ("2", "Song B", "1.00/4.00", "- energy close (+0.5)")]
    table = render_table(HEADERS, rows, aligns=["r", "l", "r", "l"], max_width=100)
    assert len({len(line) for line in lines_of(table)}) == 1


def test_multi_line_cells_make_taller_rows_and_keep_all_text():
    rows = [("1", "Title\nby Someone", "2.00/4.00", "- first reason\n- second reason")]
    table = render_table(HEADERS, rows, max_width=100)
    body = [line for line in lines_of(table) if line.startswith("| 1") or line.startswith("|   ")]
    assert len(body) == 2
    for text in ("Title", "by Someone", "first reason", "second reason"):
        assert text in table


def test_long_reasons_wrap_to_fit_the_max_width_with_a_hanging_indent():
    long_reason = "- " + "word " * 30
    table = render_table(HEADERS, [("1", "Song", "1.00/4.00", long_reason)], max_width=60)
    assert all(len(line) <= 60 for line in lines_of(table))
    reason_lines = [line.split("| ")[-1].rstrip(" |") for line in lines_of(table)
                    if "word" in line]
    assert len(reason_lines) > 1
    assert reason_lines[0].startswith("- ")
    assert all(line.startswith("  ") for line in reason_lines[1:])


def test_right_aligned_column_lines_up_on_the_right():
    rows = [("1", "A", "9.99/9.99", "x"), ("2", "B", "1/9", "y")]
    table = render_table(HEADERS, rows, aligns=["r", "l", "r", "l"], max_width=100)
    assert "|       1/9 |" in table


def test_default_output_is_not_a_table_and_table_flag_adds_reasons(capsys, monkeypatch):
    monkeypatch.setenv("COLUMNS", "200")
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35}
    results = recommend_songs(prefs, songs, 5)

    print_recommendations(prefs, results)
    plain = capsys.readouterr().out
    assert "+---" not in plain and "Reasons:" in plain

    print_recommendations(prefs, results, as_table=True)
    table = capsys.readouterr().out
    assert "| Reasons" in table
    assert "genre match: lofi (+1.0)" in table
    assert "energy 0.35 vs target 0.35 (+2.00)" in table
    assert "Summary: top pick Library Rain (4.00/4.00)" in table
