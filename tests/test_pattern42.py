"""Tests for mazegen.pattern42."""

from __future__ import annotations

from mazegen.pattern42 import PATTERN_HEIGHT, PATTERN_WIDTH, get_blocked_cells


def test_pattern_fits_centered_in_large_enough_grid() -> None:
    width, height = 20, 12
    blocked = get_blocked_cells(width, height, entry=(0, 0), exit_=(19, 11))

    assert len(blocked) > 0
    xs = [x for x, _ in blocked]
    ys = [y for _, y in blocked]
    # The bounding box of the pattern must match its declared dimensions.
    assert max(xs) - min(xs) + 1 <= PATTERN_WIDTH
    assert max(ys) - min(ys) + 1 <= PATTERN_HEIGHT
    # And it must be roughly centered (allowing for integer-division offset).
    expected_offset_x = (width - PATTERN_WIDTH) // 2
    expected_offset_y = (height - PATTERN_HEIGHT) // 2
    assert min(xs) == expected_offset_x
    assert min(ys) == expected_offset_y


def test_pattern_omitted_when_grid_too_small() -> None:
    blocked = get_blocked_cells(5, 5, entry=(0, 0), exit_=(4, 4))
    assert blocked == set()


def test_pattern_omitted_when_overlapping_entry() -> None:
    width, height = 20, 12
    offset_x = (width - PATTERN_WIDTH) // 2
    offset_y = (height - PATTERN_HEIGHT) // 2
    # Entry placed right on top of a pattern cell (top-left corner of "4").
    blocked = get_blocked_cells(
        width, height, entry=(offset_x, offset_y), exit_=(19, 11)
    )
    assert blocked == set()


def test_pattern_omitted_when_overlapping_exit() -> None:
    width, height = 20, 12
    offset_x = (width - PATTERN_WIDTH) // 2
    offset_y = (height - PATTERN_HEIGHT) // 2
    blocked = get_blocked_cells(
        width, height, entry=(0, 0), exit_=(offset_x, offset_y)
    )
    assert blocked == set()
