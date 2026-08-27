from mazegen import MazeGenerator


NORTH = 1
EAST = 2
SOUTH = 4
COLORS = [
    "\033[36m",        # cyan
    "\033[38;5;205m",  # pink
    "\033[38;5;129m",  # purple
    "\033[38;5;208m",  # orange
]
PATTERN42_COLOR = "\033[48;5;220m"
RESET = "\033[0m"
ENTRY_COLOR = "\033[32m"  # green
EXIT_COLOR = "\033[31m"   # red
PATH_COLOR = "\033[93m"   # bright yellow


def draw_row(
    generator: MazeGenerator,
    y: int,
    color: str = "",
) -> str:
    """Draw one horizontal wall row of the maze."""
    row = color
    for x in range(generator.width):
        walls = generator.get_cell_walls(x, y)
        if walls & NORTH:
            row += "+---"
        else:
            row += "+   "
    row += "+"
    return row + RESET


def draw_cells(
    generator: MazeGenerator,
    y: int,
    path_cells: list[tuple[int, int]] | None = None,
    color: str = "",
) -> str:
    """Draw one row of cells, including entry, exit, path and 42 pattern."""
    row = color + "|"
    entry = generator.get_entry()
    exit_ = generator.get_exit()
    pattern42 = generator.get_blocked_cells()
    for x in range(generator.width):
        walls = generator.get_cell_walls(x, y)
        if (x, y) == entry:
            row += f"{ENTRY_COLOR} E {color}"
        elif (x, y) == exit_:
            row += f"{EXIT_COLOR} X {color}"
        elif path_cells and (x, y) in path_cells:
            row += f"{PATH_COLOR} ● {color}"
        elif (x, y) in pattern42:
            row += f"{PATTERN42_COLOR}   \033[0m{color}"
        else:
            row += "   "
        if walls & EAST:
            row += "|"
        else:
            row += " "
    return row + RESET


def draw_bottom_row(
    generator: MazeGenerator,
    y: int,
    color: str = "",
) -> str:
    """Draw the bottom walls of one row of cells."""
    row = color
    for x in range(generator.width):
        walls = generator.get_cell_walls(x, y)
        if walls & SOUTH:
            row += "+---"
        else:
            row += "+   "
    row += "+"
    return row + RESET


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


def draw_maze(
    generator: MazeGenerator,
    show_path: bool = False,
    color: str = "",
) -> str:
    """Draw the complete maze using the selected color."""
    path_cells = get_path_cells(generator) if show_path else None
    maze = ""
    for y in range(generator.height):
        maze += draw_row(generator, y, color) + "\n"
        maze += draw_cells(
            generator,
            y,
            path_cells,
            color,
        ) + "\n"
    maze += draw_bottom_row(
        generator,
        generator.height - 1,
        color,
    ) + "\n"
    return maze


def show_cell(generator: MazeGenerator, x: int, y: int) -> None:
    """Show the walls of one cell."""
    walls = generator.get_cell_walls(x, y)
    print(walls)
    # probablemente esta funcion desaparecera


def show_menu() -> str:
    """Display the interactive menu with colored options."""
    frame = PATH_COLOR
    title = ENTRY_COLOR
    print(f"\n{frame}+--------------------------------+{RESET}")
    print(f"{frame}|{title}{'A-Maze-ing':^32}{frame}|{RESET}")
    print(f"{frame}+--------------------------------+{RESET}")
    option_1 = f"{frame}| {COLORS[0]}1. Regenerate maze"
    option_2 = f"{frame}| {COLORS[1]}2. Show/hide path"
    option_3 = f"{frame}| {COLORS[2]}3. Rotate colors"
    option_4 = f"{frame}| {COLORS[3]}4. Exit"
    print(f"{option_1}{frame}             |{RESET}")
    print(f"{option_2}{frame}              |{RESET}")
    print(f"{option_3}{frame}               |{RESET}")
    print(f"{option_4}{frame}                        |{RESET}")
    print(f"{frame}+--------------------------------+{RESET}")
    print()
    return input(f"{frame}Choose an option: {RESET}")


def run_menu(generator: MazeGenerator) -> str:
    """Run the interactive menu until the user chooses to exit."""
    show_path = False
    color_index = 0
    while True:
        print(draw_maze(generator, show_path, COLORS[color_index]))
        choice = show_menu()
        if choice == "1":
            generator.generate()
            show_path = False
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_index = (color_index + 1) % len(COLORS)
        elif choice == "4":
            return "4"
        else:
            print("Invalid option")
