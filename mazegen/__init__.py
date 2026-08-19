"""Reusable maze generation package.

Basic usage:

    from mazegen import MazeGenerator

    gen = MazeGenerator(width=15, height=10, entry=(0, 0), exit_=(14, 9),
                         perfect=True, seed=42)
    gen.generate()
    print(gen.get_solution())        # e.g. "EESSEESS..."
    print(gen.get_cell_walls(0, 0))  # e.g. 9 (bits N,E,S,W)
"""

from mazegen.generator import MazeGenerator

__all__ = ["MazeGenerator"]
__version__ = "0.2.0"
