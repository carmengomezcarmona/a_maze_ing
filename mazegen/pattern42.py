"""Compute which cells must stay fully closed to draw the '42' pattern.

The pattern is a simple 7x5-pixel block font per digit, combined with a
1-column gap. Those cells are never carved by the generator, so they stay
at their initial value (all 4 walls closed) and become visible as a solid
'42' shape once the maze is rendered.
"""

from __future__ import annotations

# 1 = cell must stay fully closed (part of the digit), 0 = free cell.
_DIGIT_4 = [
    "1 0 0 1 0",
    "1 0 0 1 0",
    "1 0 0 1 0",
    "1 1 1 1 1",
    "0 0 0 1 0",
    "0 0 0 1 0",
    "0 0 0 1 0",
]
_DIGIT_2 = [
    "1 1 1 1 0",
    "0 0 0 1 0",
    "0 0 0 1 0",
    "1 1 1 1 0",
    "1 0 0 0 0",
    "1 0 0 0 0",
    "1 1 1 1 0",
]
_GAP = 1  # empty columns between the two digits


def _build_pattern() -> list[list[bool]]:
    """Combine the two digit bitmaps into a single '42' boolean grid."""
    rows: list[list[bool]] = []
    for row_4, row_2 in zip(_DIGIT_4, _DIGIT_2):
        cells_4 = [c == "1" for c in row_4.split()]
        cells_2 = [c == "1" for c in row_2.split()]
        rows.append(cells_4 + [False] * _GAP + cells_2)
    return rows


_PATTERN: list[list[bool]] = _build_pattern()
PATTERN_HEIGHT = len(_PATTERN)
PATTERN_WIDTH = len(_PATTERN[0])


def get_blocked_cells(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
) -> set[tuple[int, int]]:
    """Return the (x, y) cells that must stay fully closed to draw '42'.

    If the maze is too small, or the pattern would overlap entry/exit, the
    pattern is omitted (as explicitly allowed by the subject) and a note
    is printed on the console.
    """
    if width < PATTERN_WIDTH or height < PATTERN_HEIGHT:
        print(
            f"Note: maze too small ({width}x{height}) to fit the '42' "
            f"pattern ({PATTERN_WIDTH}x{PATTERN_HEIGHT} needed); omitting it."
        )
        return set()

    offset_x = (width - PATTERN_WIDTH) // 2
    offset_y = (height - PATTERN_HEIGHT) // 2

    blocked = {
        (offset_x + x, offset_y + y)
        for y, row in enumerate(_PATTERN)
        for x, is_blocked in enumerate(row)
        if is_blocked
    }

    if entry in blocked or exit_ in blocked:
        print("Note: '42' pattern would overlap entry/exit; omitting it.")
        return set()

    return blocked
