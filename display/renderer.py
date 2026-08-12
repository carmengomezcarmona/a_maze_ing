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


def draw_cells(generator: MazeGenerator, y: int) -> str:
    """Draw one row of cells and their east walls."""
    row = "|"
    for x in range(generator.width):
        walls = generator.get_cell_walls(x, y)
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


def draw_maze(generator: MazeGenerator) -> str:
    """Draw the complete maze."""
    maze = ""
    for y in range(generator.height):
        maze += draw_row(generator, y) + "\n"
        maze += draw_cells(generator, y) + "\n"
    maze += draw_bottom_row(generator, generator.height - 1) + "\n"
    return maze


def show_cell(generator: MazeGenerator, x: int, y: int) -> None:
    """Show the walls of one cell."""
    walls = generator.get_cell_walls(x, y)
    print(walls)
