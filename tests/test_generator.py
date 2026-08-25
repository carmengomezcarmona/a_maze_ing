"""Tests for mazegen.generator.MazeGenerator."""

from __future__ import annotations

import pytest

from mazegen import MazeGenerator
from mazegen.exceptions import MazeGenerationError

WIDTH, HEIGHT = 15, 10
ENTRY, EXIT = (0, 0), (14, 9)


# --------------------------------------------------------------------- #
# Constructor / validation
# --------------------------------------------------------------------- #

def test_invalid_dimensions_raise() -> None:
    with pytest.raises(MazeGenerationError):
        MazeGenerator(width=0, height=5, entry=(0, 0), exit_=(0, 1))


def test_entry_outside_bounds_raises() -> None:
    with pytest.raises(MazeGenerationError):
        MazeGenerator(width=5, height=5, entry=(10, 0), exit_=(0, 1))


def test_exit_outside_bounds_raises() -> None:
    with pytest.raises(MazeGenerationError):
        MazeGenerator(width=5, height=5, entry=(0, 0), exit_=(10, 1))


def test_entry_equals_exit_raises() -> None:
    with pytest.raises(MazeGenerationError):
        MazeGenerator(width=5, height=5, entry=(0, 0), exit_=(0, 0))


def test_all_cells_start_fully_closed() -> None:
    gen = MazeGenerator(width=4, height=4, entry=(0, 0), exit_=(3, 3), seed=1)
    for y in range(4):
        for x in range(4):
            assert gen.get_cell_walls(x, y) == 15


# --------------------------------------------------------------------- #
# Perfect mode: spanning tree properties
# --------------------------------------------------------------------- #

def test_perfect_maze_has_solution() -> None:
    gen = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, perfect=True, seed=42)
    gen.generate()
    solution = gen.get_solution()
    assert len(solution) > 0
    assert set(solution) <= {"N", "E", "S", "W"}


def test_perfect_maze_has_exactly_width_height_minus_one_edges() -> None:
    """A spanning tree over N cells has exactly N-1 edges (open walls)."""
    gen = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, perfect=True, seed=7)
    gen.generate()

    open_edges = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            walls = gen.get_cell_walls(x, y)
            if x + 1 < WIDTH and not (walls & 2):  # East open
                open_edges += 1
            if y + 1 < HEIGHT and not (walls & 4):  # South open
                open_edges += 1

    blocked_count = len(gen.get_blocked_cells())
    reachable_cells = WIDTH * HEIGHT - blocked_count
    assert open_edges == reachable_cells - 1


def test_wall_coherence_between_neighbours() -> None:
    """If a cell has its East wall closed, its East neighbour must have
    its West wall closed too (and vice versa for South/North)."""
    gen = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, perfect=False, seed=3)
    gen.generate()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            walls = gen.get_cell_walls(x, y)
            if x + 1 < WIDTH:
                east_closed = bool(walls & 2)
                west_of_neighbour_closed = bool(gen.get_cell_walls(x + 1, y)
                                                & 8)
                assert east_closed == west_of_neighbour_closed
            if y + 1 < HEIGHT:
                south_closed = bool(walls & 4)
                north_of_neighbour_closed = bool(gen.get_cell_walls(x, y + 1)
                                                 & 1)
                assert south_closed == north_of_neighbour_closed


def test_reproducibility_same_seed_same_maze() -> None:
    gen1 = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, perfect=True, seed=123)
    gen1.generate()
    gen2 = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, perfect=True, seed=123)
    gen2.generate()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            assert gen1.get_cell_walls(x, y) == gen2.get_cell_walls(x, y)
    assert gen1.get_solution() == gen2.get_solution()


def test_different_seeds_usually_differ() -> None:
    gen1 = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, perfect=True, seed=1)
    gen1.generate()
    gen2 = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, perfect=True, seed=2)
    gen2.generate()

    walls1 = [gen1.get_cell_walls(x, y) for y in range(HEIGHT)
              for x in range(WIDTH)]
    walls2 = [gen2.get_cell_walls(x, y) for y in range(HEIGHT)
              for x in range(WIDTH)]
    assert walls1 != walls2


# --------------------------------------------------------------------- #
# Non-perfect / Pac-Man mode
# --------------------------------------------------------------------- #

def test_non_perfect_maze_has_more_open_edges_than_perfect() -> None:
    """PERFECT=False must add at least one loop (extra open edge)."""
    perfect = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, perfect=True, seed=9)
    perfect.generate()
    non_perfect = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT,
                                perfect=False, seed=9)
    non_perfect.generate()

    def count_open_edges(gen: MazeGenerator) -> int:
        total = 0
        for y in range(HEIGHT):
            for x in range(WIDTH):
                walls = gen.get_cell_walls(x, y)
                if x + 1 < WIDTH and not (walls & 2):
                    total += 1
                if y + 1 < HEIGHT and not (walls & 4):
                    total += 1
        return total

    assert count_open_edges(non_perfect) > count_open_edges(perfect)


def test_no_forbidden_3x3_open_block_in_non_perfect_mode() -> None:
    """The corridor-width rule: never a fully-open 3x3 block of cells."""
    gen = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, perfect=False, seed=5)
    gen.generate()

    def fully_open(top_x: int, top_y: int) -> bool:
        for y in range(top_y, top_y + 3):
            for x in range(top_x, top_x + 3):
                walls = gen.get_cell_walls(x, y)
                if x + 1 < top_x + 3 and walls & 2:
                    return False
                if y + 1 < top_y + 3 and walls & 4:
                    return False
        return True

    violations = [
        (x, y)
        for y in range(HEIGHT - 2)
        for x in range(WIDTH - 2)
        if fully_open(x, y)
    ]
    assert violations == []


# --------------------------------------------------------------------- #
# "42" pattern
# --------------------------------------------------------------------- #

def test_42_pattern_cells_stay_fully_closed() -> None:
    gen = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, perfect=True, seed=11)
    gen.generate()
    blocked = gen.get_blocked_cells()
    assert len(blocked) > 0  # this grid is big enough to fit the pattern
    for x, y in blocked:
        assert gen.get_cell_walls(x, y) == 15


def test_42_pattern_omitted_when_maze_too_small() -> None:
    gen = MazeGenerator(width=5, height=5, entry=(0, 0), exit_=(4, 4), seed=1)
    gen.generate()
    assert gen.get_blocked_cells() == set()


# --------------------------------------------------------------------- #
# Solver
# --------------------------------------------------------------------- #

def test_solution_path_matches_open_walls() -> None:
    """Walking the returned solution string must stay inside the maze and
    only cross walls that are actually open."""
    gen = MazeGenerator(WIDTH, HEIGHT, ENTRY, EXIT, perfect=True, seed=17)
    gen.generate()

    deltas = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    bits = {"N": 1, "E": 2, "S": 4, "W": 8}

    x, y = gen.get_entry()
    for step in gen.get_solution():
        walls = gen.get_cell_walls(x, y)
        assert not (walls & bits[step]), f"wall {step} is closed at ({x},{y})"
        dx, dy = deltas[step]
        x, y = x + dx, y + dy
        assert 0 <= x < WIDTH and 0 <= y < HEIGHT

    assert (x, y) == gen.get_exit()


def test_get_solution_before_generate_raises() -> None:
    gen = MazeGenerator(width=4, height=4, entry=(0, 0), exit_=(3, 3), seed=1)
    with pytest.raises(MazeGenerationError):
        gen.get_solution()
