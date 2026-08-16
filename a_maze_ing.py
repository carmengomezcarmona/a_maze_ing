#!/usr/bin/env python3
"""A-Maze-ing: generate a maze from a config file and write it to disk.

Usage:
    python3 a_maze_ing.py config.txt
"""

import sys

# imports from app folder
from app.config_parser import parse_config
from app.errors import ConfigError
from app.output_writer import write_maze
from display.renderer import run_menu

# imports from mazegen folder
from mazegen import MazeGenerator
from mazegen.exceptions import MazeGenerationError


def main(argv: list[str]) -> int:
    """Run the program. Returns the process exit code."""
    if len(argv) != 2:
        print(f"Usage: python3 {argv[0]} <config_file>", file=sys.stderr)
        return 1

    config_path = argv[1]

    try:
        config = parse_config(config_path)
    except ConfigError as exc:
        print(f"Error: invalid configuration: {exc}", file=sys.stderr)
        return 1

    try:
        generator = MazeGenerator(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit_=config.exit_,
            perfect=config.perfect,
            seed=config.seed,
        )
        generator.generate()
    except MazeGenerationError as exc:
        print(f"Error: could not generate maze: {exc}", file=sys.stderr)
        return 1

    try:
        write_maze(config.output_file, generator)
    except OSError as exc:
        print(f"Error: could not write output file: {exc}", file=sys.stderr)
        return 1

    print(f"Maze written to {config.output_file}")
    print(f"Solution ({len(generator.get_solution())} steps): "
          f"{generator.get_solution()}")
    while True:
        choice = run_menu(generator)
        if choice == "4":
            return 0
        if choice == "1":
            generator = MazeGenerator(
                width=config.width,
                height=config.height,
                entry=config.entry,
                exit_=config.exit_,
                perfect=config.perfect,
                seed=config.seed,
            )
            generator.generate()
            write_maze(config.output_file, generator)
            print(f"Maze written to {config.output_file}")
            print(f"Solution ({len(generator.get_solution())} steps): "
                  f"{generator.get_solution()}")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
