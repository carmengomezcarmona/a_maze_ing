*This project has been created as part of the 42 curriculum by carmgome and gapostig*

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
