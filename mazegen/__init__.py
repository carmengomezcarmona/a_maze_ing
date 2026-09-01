"""Reusable maze generation package."""

from .generator import MazeGenerator
from .exceptions import MazeGenerationError
from .pattern42 import get_blocked_cells

__all__ = ["MazeGenerator", "MazeGenerationError", "get_blocked_cells"]
__version__ = "0.2.0"
