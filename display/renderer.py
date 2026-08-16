from mazegen import MazeGenerator


NORTH = 1
EAST = 2
SOUTH = 4


def draw_row(generator: MazeGenerator, y: int) -> str:
    """Draw one horizontal wall row of the maze."""
    row = ""
    for x in range(generator.width):
        walls = generator.get_cell_walls(x, y)
        if walls & NORTH:
            row += "+---"
        else:
            row += "+   "
    row += "+"
    return row


def draw_cells(
    generator: MazeGenerator,
    y: int,
    path_cells: list[tuple[int, int]] | None = None,
) -> str:
    """Draw one row of cells and their east walls."""
    row = "|"
    for x in range(generator.width):
        walls = generator.get_cell_walls(x, y)

        if path_cells and (x, y) in path_cells:
            row += " · "
        else:
            row += "   "

        if walls & EAST:
            row += "|"
        else:
            row += " "
    return row


def draw_bottom_row(generator: MazeGenerator, y: int) -> str:
    """Draw the bottom walls of one row of cells."""
    row = ""
    for x in range(generator.width):
        walls = generator.get_cell_walls(x, y)
        if walls & SOUTH:
            row += "+---"
        else:
            row += "+   "
    row += "+"
    return row


def get_path_cells(generator: MazeGenerator) -> list[tuple[int, int]]:
    """Return the cells visited by the solution path."""
    x, y = generator.get_entry()
    path = [(x, y)]

    for direction in generator.get_solution():
        if direction == "E":
            x += 1
        elif direction == "W":
            x -= 1
        elif direction == "S":
            y += 1
        elif direction == "N":
            y -= 1

        path.append((x, y))

    return path


def draw_maze(generator: MazeGenerator) -> str:
    """Draw the complete maze."""
    maze = ""
    path_cells = get_path_cells(generator)

    for y in range(generator.height):
        maze += draw_row(generator, y) + "\n"
        maze += draw_cells(generator, y, path_cells) + "\n"
    maze += draw_bottom_row(generator, generator.height - 1) + "\n"
    return maze


def show_cell(generator: MazeGenerator, x: int, y: int) -> None:
    """Show the walls of one cell."""
    walls = generator.get_cell_walls(x, y)
    print(walls)
