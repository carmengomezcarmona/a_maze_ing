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
# Local column index of the gap between '4' and '2' (always the exact
# middle of the pattern, since it's built as digit + 1-col gap + digit
# with two equally-wide digits). This column is open on every row.
_GAP_COLUMN = PATTERN_WIDTH // 2


def get_blocked_cells(
    width: int,
    height: int,
    required_open: set[tuple[int, int]],
) -> set[tuple[int, int]]:
    """Return the (x, y) cells that must stay fully closed to draw '42'.

    The pattern is always placed dead-centre in the grid -- it is never
    shifted to dodge required-open cells. To make that compatible with
    Pac-Man mode (where the grid's own centre cell must stay open), the
    horizontal offset is computed as `width // 2 - PATTERN_WIDTH // 2`
    rather than the more naive `(width - PATTERN_WIDTH) // 2`. Both give
    a "centered" placement, but only the first one guarantees that the
    pattern's own gap column (between '4' and '2', open on every row)
    lands exactly on the grid's centre column for ANY width, odd or
    even. `(width - PATTERN_WIDTH) // 2` can be off by one cell for even
    widths, which is what used to make the pattern collide with the
    required-open centre cell.

    Args:
        width: Maze width.
        height: Maze height.
        required_open: Cells that must NOT be part of the pattern (e.g.
            entry, exit, and -- in Pac-Man mode -- the four corners and
            the centre cell).

    If the maze is too small, or the pattern still overlaps a
    required-open cell despite the centring guarantee above (e.g. entry
    or exit placed very close to the middle of a small grid), the
    pattern is omitted (as explicitly allowed by the subject) and a note
    is printed on the console.
    """
    if width < PATTERN_WIDTH or height < PATTERN_HEIGHT:
        print(
            f"Note: maze too small ({width}x{height}) to fit the '42' "
            f"pattern ({PATTERN_WIDTH}x{PATTERN_HEIGHT} needed); omitting it."
        )
        return set()

    offset_x = width // 2 - PATTERN_WIDTH // 2
    offset_y = height // 2 - PATTERN_HEIGHT // 2

    blocked = {
        (offset_x + x, offset_y + y)
        for y, row in enumerate(_PATTERN)
        for x, is_blocked in enumerate(row)
        if is_blocked
    }

    if blocked & required_open:
        print(
            "Note: '42' pattern would overlap a required-open cell "
            "(entry/exit/corner/centre); omitting it."
        )
        return set()

    return blocked
