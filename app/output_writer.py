"""Write the generated maze to disk in the format required by the subject.

Format reminder:
    - One hex digit per cell, row by row.
    - One empty line.
    - Entry coordinates ("x,y").
    - Exit coordinates ("x,y").
    - Shortest path as N/E/S/W letters.
    - Every line ends with '\\n'.
"""

from __future__ import annotations

from mazegen import MazeGenerator


def write_maze(output_path: str, generator: MazeGenerator) -> None:
    """Write `generator`'s maze to `output_path`.

    Raises:
        OSError: If the file can't be written (permissions, invalid path...).
    """
    lines: list[str] = []
    for y in range(generator.height):
        row = "".join(
            format(generator.get_cell_walls(x, y), "x")
            for x in range(generator.width)
        )
        lines.append(row)

    lines.append("")  # empty separator line
    entry_x, entry_y = generator.get_entry()
    exit_x, exit_y = generator.get_exit()
    lines.append(f"{entry_x},{entry_y}")
    lines.append(f"{exit_x},{exit_y}")
    lines.append(generator.get_solution())

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
