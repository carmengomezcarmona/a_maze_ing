*This project has been created as part of the 42 curriculum by carmgome, gapostig*

# A_MAZE_ING

## Description

A-Maze-ing is a Python program that reads a configuration file and generates a maze according to the specified parameters. The generated maze is saved to an output file, and the program calculates the shortest path from the entry to the exit.

The project also includes an interactive terminal display where the generated maze can be viewed and different options can be selected.

## Instruction

The project can be run using the provided Makefile:

```bash
make run
```

By default, the program uses `config.txt` as the configuration file.

It is also possible to run the program directly:

```bash
python3 a_maze_ing.py config.txt
```

The program reads the configuration, generates the maze and writes the result to `maze.txt`. The maze is then displayed in the terminal with an interactive menu.

The menu provides the following options:

* Regenerate the maze
* Show or hide the solution path
* Rotate the maze colors
* Exit the program

## Structure and format of the config file

The configuration file uses a simple `KEY=VALUE` format.

Example:

```text
WIDTH=10
HEIGHT=8
ENTRY=0,0
EXIT=9,7
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

The parameters are:

* `WIDTH`: width of the maze in cells.
* `HEIGHT`: height of the maze in cells.
* `ENTRY`: coordinates of the entry cell, using the format `x,y`.
* `EXIT`: coordinates of the exit cell, using the format `x,y`.
* `OUTPUT_FILE`: name of the file where the generated maze is saved.
* `PERFECT`: determines whether the maze is generated as a perfect maze, without loops.
* `SEED`: optional value used to make maze generation reproducible. Using the same configuration and seed produces the same maze.

## The maze generation algorithm chosen

The maze is generated using the **recursive backtracker** algorithm.

The generator starts with a grid where all cells have their four walls closed. It starts from the entry cell and repeatedly chooses an unvisited neighbouring cell. When moving to a new cell, the wall between the two cells is removed.

When the generator reaches a cell where there are no unvisited neighbours, it goes back to a previous cell and continues searching for another possible direction.

When `PERFECT=True`, this process creates a perfect maze with no loops and a unique path between two cells.

When `PERFECT=False`, the generator can remove additional walls after the initial maze has been created. This creates loops and therefore alternative routes through the maze.

The generator also supports the special `42` pattern. The cells belonging to the pattern are kept fully closed and are not carved during maze generation, allowing the `42` shape to remain visible in the generated maze.

### Why this algorithm

We chose the recursive backtracker because it is simple to implement and extend, while producing long, winding corridors that are easy to read and enjoyable to solve. Unlike Kruskal's and Prim's algorithms, it needs no additional data structures and can easily skip the cells reserved for the "42" pattern or open extra walls when `PERFECT=False`. Its main drawback is that it may create long corridors with few branches, but this was considered acceptable for the project's goals.

## What part of the code is reusable

The `mazegen` package was designed to be reusable independently from the main application.

The `MazeGenerator` class contains the core maze generation and solving logic. It can be imported and used by other Python programs without depending on the configuration parser, output writer or terminal renderer.

For example:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=15,
    height=10,
    entry=(0, 0),
    exit_=(14, 9),
    perfect=True,
    seed=42,
)

generator.generate()
```

The generator provides methods to access the maze walls, entry and exit coordinates, the solution path and the cells used for the `42` pattern.

This separation makes the maze generation logic reusable in other applications or interfaces.

## Planning and how it evolved

The project was developed progressively, with the main components being implemented and tested separately before being integrated.

The initial work focused on establishing the project structure and implementing configuration parsing and error handling. The maze generator was then developed to create the maze and calculate a solution path.

Once the generation pipeline was working, the output writer was added to produce the file required by the subject.

The project was then extended with a terminal renderer to display the maze visually. An interactive menu was added afterwards, allowing the user to regenerate the maze, show or hide the solution path, change the display colors and exit the program.

Later iterations added support for the `42` pattern and additional generation rules, together with automated tests for the generator and the pattern.

The project evolved through incremental testing and integration rather than implementing the complete application at once.

## What worked well and what could be improved

The separation of the project into different components worked particularly well. Configuration parsing, maze generation, output writing and rendering have clearly defined responsibilities, which makes the code easier to understand, test and maintain.

The reusable `MazeGenerator` class also allowed us to keep the core generation and solving logic independent from the user interface. This made it easier to integrate the generator with both the output system and the interactive terminal renderer.

Developing the project incrementally was also effective. Each component could be tested independently before being integrated with the rest of the application. Automated tests helped us verify the behaviour of the maze generator and the `42` pattern.

The terminal renderer was another successful part of the project. It provides a visual representation of the maze and includes an interactive menu with options to regenerate the maze, show or hide the solution path, change the display colors and exit the program.

One area that could be improved in a future version would be the user interface, for example by providing additional visual or interactive features. The internal architecture could also be extended if the project were to support other types of maze generation algorithms or additional output formats.

## Have You used any specific tools? Which ones?

The project was developed using Python 3 and several tools to help with development, testing and collaboration.

* **Git and GitHub** were used for version control and collaboration between team members.
* **Visual Studio Code** was used as the main code editor.
* **flake8** was used to check code style and maintain consistent formatting.
* **mypy** was used for static type checking, including strict mode validation.
* **pytest** was used to create and run automated tests.
* **pdb** was used when debugging was necessary.
* The **Makefile** was used to simplify common commands such as running the project, cleaning generated files and performing code quality checks.
* The **terminal** was used extensively to run the program, test different configurations and inspect the generated output.

AI-assisted tools were also used during development for explanations, debugging assistance and documentation support. Their suggestions were reviewed and adapted to the project's requirements.


## The Project Management

    - The Visual Part (/display  y /app) - *carmgome*
    - The Motor part (/mazegen) - *gapostig*

## Resources

The following resources were useful during the development of the project:

* The official Python documentation.
* The documentation and project requirements provided by the 42 curriculum.
* Python documentation about modules, packages, classes and type hints.
* Documentation and references about recursive algorithms and graph traversal.
* References about Breadth-First Search (BFS), used to calculate the shortest path between the entry and exit.
* Git and GitHub documentation for version control and collaboration.
* Documentation for `flake8`, `mypy` and `pytest`.

The project was also developed through practical experimentation, testing different configurations and validating the generated mazes against the project requirements.
