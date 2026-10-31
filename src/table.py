"""A small dependency-free ASCII table renderer for the terminal output."""

import shutil
import textwrap
from typing import List, Optional, Sequence


def _wrap_cell(text: str, width: int) -> List[str]:
    """Wraps a cell to a column width. Bullet lines ("- ...") get a hanging indent."""
    lines = []
    for line in str(text).split("\n"):
        indent = "  " if line.startswith("- ") else ""
        lines.extend(textwrap.wrap(line, width, subsequent_indent=indent) or [""])
    return lines


def render_table(
    headers: Sequence[str],
    rows: Sequence[Sequence[str]],
    aligns: Optional[Sequence[str]] = None,
    max_width: Optional[int] = None,
    flex_col: int = -1,
    min_flex_width: int = 24,
) -> str:
    """
    Renders rows as a bordered ASCII table. Cells may hold several lines ("\\n").

    aligns:    one "l" or "r" per column (default: all left).
    max_width: total width allowed. Only the flex column shrinks to fit, and its
               text wraps onto more lines. Defaults to the terminal width.
    """
    count = len(headers)
    aligns = list(aligns) if aligns else ["l"] * count
    flex_col %= count
    if max_width is None:
        max_width = shutil.get_terminal_size(fallback=(100, 24)).columns

    widths = []
    for i, header in enumerate(headers):
        lines = [header] + [line for row in rows for line in str(row[i]).split("\n")]
        widths.append(max(len(line) for line in lines))

    overhead = 3 * count + 1  # "| " and " |" around each cell, "|" between
    others = sum(widths) - widths[flex_col]
    room = max_width - overhead - others
    widths[flex_col] = min(widths[flex_col], max(room, min_flex_width, len(headers[flex_col])))

    border = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def format_line(cells: Sequence[str]) -> str:
        padded = [
            cell.rjust(w) if align == "r" else cell.ljust(w)
            for cell, w, align in zip(cells, widths, aligns)
        ]
        return "| " + " | ".join(padded) + " |"

    out = [border, format_line([h.ljust(w) if a == "l" else h.rjust(w)
                                for h, w, a in zip(headers, widths, aligns)]), border]
    for row in rows:
        wrapped = [_wrap_cell(cell, w) for cell, w in zip(row, widths)]
        for i in range(max(len(cell) for cell in wrapped)):
            out.append(format_line([cell[i] if i < len(cell) else "" for cell in wrapped]))
        out.append(border)
    return "\n".join(out)
