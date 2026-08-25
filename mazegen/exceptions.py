"""Custom exceptions raised by the mazegen package."""


class MazeGenerationError(Exception):
    """Raised when a maze cannot be generated with the given parameters."""
    def __init__(self, message: str = "Unknown Maze generation error"):
        super().__init__(message)
