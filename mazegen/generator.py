"""Core maze generation logic.

Current state:
- Perfect mode (PERFECT=True): classic recursive backtracker -> spanning
  tree, single path between any two cells.
- Non-perfect / Pac-Man mode (PERFECT=False): the same spanning tree, with
  extra random walls knocked down to create loops, WITHOUT ever creating a
  fully-open 3x3 block of cells (corridor-width rule).
- The '42' pattern is carved by simply never visiting the cells that make
  up the digits (see mazegen.pattern42): they keep all 4 walls closed.

What this version does NOT do yet (left as TODO for later iterations):
- Guarantee the four corners + centre are open, and dead-ends are rare,
  as required for the Pac-Man mode.

Keeping that out for now lets the whole pipeline (config -> generation ->
output file -> display) work end to end; the missing rule can be added
inside `_add_loops()` without changing the public interface used by the
rest of the project.
"""

from __future__ import annotations

import random
from typing import Optional

from mazegen.exceptions import MazeGenerationError
from mazegen.pattern42 import get_blocked_cells

# Bit values for each direction, and the bit used by the neighbour on the
# opposite side of the same wall (walls are shared between two cells).
_NORTH, _EAST, _SOUTH, _WEST = 1, 2, 4, 8
_DIRECTIONS: dict[str, tuple[int, int, int, int]] = {
    "N": (0, -1, _NORTH, _SOUTH),
    "E": (1, 0, _EAST, _WEST),
    "S": (0, 1, _SOUTH, _NORTH),
    "W": (-1, 0, _WEST, _EAST),
}

# Size of the "open area" that is forbidden (see IV.4 of the subject:
# corridors can be at most 2 cells wide, so a full 3x3 open block is not
# allowed, but 2x3 / 3x2 are fine).
_FORBIDDEN_BLOCK_SIZE = 3


class MazeGenerator:
    """Generate, store and solve a rectangular maze.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        entry: (x, y) coordinates of the entry cell.
        exit_: (x, y) coordinates of the exit cell.
        perfect: If True, generate a perfect maze (no loops).
        seed: Optional seed for reproducibility.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:
        """Validate parameters and prepare an empty (fully-walled) grid.

        Raises:
            MazeGenerationError: If the parameters can't produce a valid maze.
        """
        if width <= 0 or height <= 0:
            raise MazeGenerationError("width and height must be positive")
        if not self._in_bounds(entry, width, height):
            raise MazeGenerationError(f"entry {entry} is outside the maze")
        if not self._in_bounds(exit_, width, height):
            raise MazeGenerationError(f"exit {exit_} is outside the maze")
        if entry == exit_:
            raise MazeGenerationError("entry and exit must be different cells")

        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.perfect = perfect
        self.seed = seed
        self._rng = random.Random(seed)

        # Every cell starts fully closed (all 4 walls up): bits 1+2+4+8 = 15.
        self._walls: dict[tuple[int, int], int] = {
            (x, y): _NORTH | _EAST | _SOUTH | _WEST
            for y in range(height)
            for x in range(width)
        }

        # Cells that make up the "42" pattern: never carved, stay closed.
        self._blocked: set[tuple[int, int]] = get_blocked_cells(
            width, height, entry, exit_
        )

        self._generated = False
        self._solution: str = ""

    @staticmethod
    def _in_bounds(cell: tuple[int, int], width: int, height: int) -> bool:
        """Return True if `cell` lies within a width x height grid."""
        x, y = cell
        return 0 <= x < width and 0 <= y < height

    def generate(self) -> None:
        """Generate the maze in place (fills the internal wall grid)."""
        self._carve_perfect_maze()
        if not self.perfect:
            self._add_loops()
        self._generated = True
        self._solution = self._solve()

    def _carve_perfect_maze(self) -> None:
        """Recursive backtracker: produces a spanning tree (perfect maze).

        Cells in `self._blocked` (the '42' pattern) are treated as already
        visited, so the algorithm never enters or carves them: they stay
        fully closed.
        """
        start = self.entry
        visited = {start} | self._blocked
        stack = [start]

        while stack:
            x, y = stack[-1]
            neighbours = []
            for direction, (dx, dy, _, _) in _DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                if self._in_bounds((nx, ny), self.width, self.height):
                    if (nx, ny) not in visited:
                        neighbours.append((direction, nx, ny))

            if not neighbours:
                stack.pop()
                continue

            direction, nx, ny = self._rng.choice(neighbours)
            self._open_wall((x, y), direction)
            visited.add((nx, ny))
            stack.append((nx, ny))

    def _open_wall(self, cell: tuple[int, int], direction: str) -> None:
        """Remove the wall between `cell` and its neighbour in `direction`."""
        dx, dy, bit_here, bit_there = _DIRECTIONS[direction]
        x, y = cell
        nx, ny = x + dx, y + dy
        self._walls[(x, y)] &= ~bit_here
        self._walls[(nx, ny)] &= ~bit_there

    def _close_wall(self, cell: tuple[int, int], direction: str) -> None:
        """Put back the wall between `cell` and its neighbour (revert)."""
        dx, dy, bit_here, bit_there = _DIRECTIONS[direction]
        x, y = cell
        nx, ny = x + dx, y + dy
        self._walls[(x, y)] |= bit_here
        self._walls[(nx, ny)] |= bit_there

    def _add_loops(self) -> None:
        """Knock down extra walls to create loops, keeping corridors
        at most 2 cells wide (never a fully-open 3x3 block).

        NOTE: minimal placeholder to satisfy "at least 2 independent
        routes". Corners/centre/dead-end requirements from the subject
        are not yet enforced here (next iteration).
        """
        candidates: list[tuple[tuple[int, int], str]] = []
        for (x, y), walls in self._walls.items():
            if (x, y) in self._blocked:
                continue
            for direction, (dx, dy, bit_here, _) in _DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                if not self._in_bounds((nx, ny), self.width, self.height):
                    continue
                if (nx, ny) in self._blocked:
                    continue
                if walls & bit_here:
                    candidates.append(((x, y), direction))

        extra_walls = max(2, (self.width * self.height) // 20)
        self._rng.shuffle(candidates)

        opened = 0
        for cell, direction in candidates:
            if opened >= extra_walls:
                break
            self._open_wall(cell, direction)
            if self._has_forbidden_open_block():
                self._close_wall(cell, direction)  # revert, try next candidate
                continue
            opened += 1

    def _has_forbidden_open_block(self) -> bool:
        """Return True if the grid contains a fully-open 3x3 cell block.

        A block is "fully open" when every internal wall between its
        cells is removed. Checking every 3x3 window catches any corridor
        that is 3+ cells wide AND 3+ cells long, which is exactly what
        the subject forbids (2x3 / 3x2 remain allowed, since neither
        dimension reaches 3x3 on both axes at once).
        """
        size = _FORBIDDEN_BLOCK_SIZE
        if self.width < size or self.height < size:
            return False
        for top_y in range(self.height - size + 1):
            for top_x in range(self.width - size + 1):
                if self._is_fully_open_block(top_x, top_y, size, size):
                    return True
        return False

    def _is_fully_open_block(
        self, top_x: int, top_y: int, w: int, h: int
    ) -> bool:
        """Return True if the w x h block starting at (top_x, top_y) has
        every internal wall open (i.e. forms one big open room)."""
        for y in range(top_y, top_y + h):
            for x in range(top_x, top_x + w):
                walls = self._walls[(x, y)]
                if x + 1 < top_x + w and walls & _EAST:
                    return False
                if y + 1 < top_y + h and walls & _SOUTH:
                    return False
        return True

    def _solve(self) -> str:
        """Breadth-first search from entry to exit.

        Returns:
            The shortest path as a string of 'N'/'E'/'S'/'W' letters.
        """
        from collections import deque

        start, target = self.entry, self.exit_
        queue: deque[tuple[int, int]] = deque([start])
        came_from: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}
        visited = {start}

        while queue:
            current = queue.popleft()
            if current == target:
                break
            x, y = current
            walls = self._walls[current]
            for direction, (dx, dy, bit_here, _) in _DIRECTIONS.items():
                if walls & bit_here:
                    continue  # wall closed on this side, can't pass
                neighbour = (x + dx, y + dy)
                if neighbour not in visited:
                    visited.add(neighbour)
                    came_from[neighbour] = (current, direction)
                    queue.append(neighbour)

        if target not in visited:
            raise MazeGenerationError("no path exists between entry and exit")

        path_letters: list[str] = []
        node = target
        while node != start:
            previous, direction = came_from[node]
            path_letters.append(direction)
            node = previous
        path_letters.reverse()
        return "".join(path_letters)

    def get_cell_walls(self, x: int, y: int) -> int:
        """Return the wall bitmask (0-15) of cell (x, y)."""
        return self._walls[(x, y)]

    def get_solution(self) -> str:
        """Return the shortest path from entry to exit as N/E/S/W letters."""
        if not self._generated:
            raise MazeGenerationError("generate() must be called first")
        return self._solution

    def get_entry(self) -> tuple[int, int]:
        """Return the (x, y) entry coordinates."""
        return self.entry

    def get_exit(self) -> tuple[int, int]:
        """Return the (x, y) exit coordinates."""
        return self.exit_

    def get_blocked_cells(self) -> set[tuple[int, int]]:
        """Return the set of cells that form the '42' pattern (if any)."""
        return set(self._blocked)
