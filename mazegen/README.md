# mazegen

Reusable maze generation engine used by the *A-Maze-ing* project (42
curriculum). Generates perfect mazes (single path, no loops) or
Pac-Man-style playable boards (full connectivity, open corners/centre,
independent loops, few dead-ends), both with wall-coherent data and the
mandatory "42" pattern of permanently-closed cells.

This package only depends on the Python standard library.

## Install

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Quick start

```python
from mazegen import MazeGenerator

gen = MazeGenerator(
    width=15,
    height=10,
    entry=(0, 0),
    exit_=(14, 9),
    perfect=True,   # False -> Pac-Man mode (loops, open corners/centre)
    seed=42,        # optional, omit for a non-reproducible maze
)
gen.generate()
```

## Custom parameters

| Parameter | Type | Meaning |
|---|---|---|
| `width`, `height` | `int` | Grid size in cells. |
| `entry`, `exit_` | `tuple[int, int]` | `(x, y)` coordinates, must be inside the grid and different from each other. |
| `perfect` | `bool` | `True` -> single path, no loops. `False` -> Pac-Man board: full connectivity, the four corners and the centre are open, at least two independent loops, dead-ends minimised. |
| `seed` | `int \| None` | Fixes the internal RNG for a reproducible maze. Omit (or `None`) for a different maze on every run. |

Invalid parameters (zero/negative size, out-of-bounds or equal entry/exit,
an unsolvable configuration) raise `mazegen.exceptions.MazeGenerationError`
with a human-readable message instead of crashing.

## Accessing the generated structure

```python
gen.get_cell_walls(x, y)   # int, 0-15: bit 1=N, 2=E, 4=S, 8=W (set = closed)
gen.get_entry()             # (x, y)
gen.get_exit()               # (x, y)
gen.get_blocked_cells()     # set[(x, y)]: cells forming the '42' pattern
                             # (empty set if it didn't fit / would overlap
                             # a required-open cell -- a note is printed)
```

## Accessing the solution

```python
gen.get_solution()  # e.g. "EESSEESS..." -- shortest entry-to-exit path
                     # as a string of 'N'/'E'/'S'/'W' letters
```

Calling `get_solution()` before `generate()` raises `MazeGenerationError`.

## Regenerating

`generate()` can be called again on the same instance (e.g. a "regenerate"
button in a UI): the grid is reset internally before carving, and the RNG
keeps advancing, so each call produces a genuinely different, valid maze.

```python
gen.generate()  # first maze
gen.generate()  # a different, equally valid maze -- same instance
```

## License

MIT — see `LICENSE.md` at the root of the source repository. Explicitly
permits reuse and redistribution by later projects.
