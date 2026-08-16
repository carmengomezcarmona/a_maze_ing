"""Parse the KEY=VALUE configuration file described in the subject."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.errors import ConfigError

_MANDATORY_KEYS = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                   "PERFECT")


@dataclass
class MazeConfig:
    """Typed, validated configuration ready to be used by the generator."""

    width: int
    height: int
    entry: tuple[int, int]
    exit_: tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None


def _read_raw_pairs(path: Path) -> dict[str, str]:
    """Read the file and return the raw KEY -> VALUE strings.

    Raises:
        ConfigError: If the file doesn't exist or a line is malformed.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise ConfigError(f"config file not found: {path}") from exc
    except OSError as exc:
        raise ConfigError(f"could not read config file: {exc}") from exc

    pairs: dict[str, str] = {}
    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigError(
                f"malformed line {line_number} in {path}: {raw_line!r}"
            )
        key, _, value = line.partition("=")
        pairs[key.strip()] = value.strip()
    return pairs


def _parse_coordinates(raw: str, key: str) -> tuple[int, int]:
    """Parse a 'x,y' string into a tuple of ints."""
    parts = raw.split(",")
    if len(parts) != 2:
        raise ConfigError(f"{key} must be formatted as 'x,y', got {raw!r}")
    try:
        x, y = int(parts[0]), int(parts[1])
    except ValueError as exc:
        raise ConfigError(f"{key} must contain integers, got {raw!r}") from exc
    return x, y


def _parse_bool(raw: str, key: str) -> bool:
    """Parse a 'True'/'False' string into a bool."""
    normalised = raw.strip().lower()
    if normalised in ("true", "1", "yes"):
        return True
    if normalised in ("false", "0", "no"):
        return False
    raise ConfigError(f"{key} must be a boolean (True/False), got {raw!r}")


def parse_config(path: str) -> MazeConfig:
    """Read and validate a configuration file.

    Args:
        path: Path to the configuration file.

    Returns:
        A validated MazeConfig ready to be passed to MazeGenerator.

    Raises:
        ConfigError: If the file is missing, malformed, or a mandatory key
            is missing or invalid.
    """
    file_path = Path(path)
    pairs = _read_raw_pairs(file_path)

    missing = [key for key in _MANDATORY_KEYS if key not in pairs]
    if missing:
        raise ConfigError(f"missing mandatory key(s): {', '.join(missing)}")

    try:
        width = int(pairs["WIDTH"])
        height = int(pairs["HEIGHT"])
    except ValueError as exc:
        raise ConfigError("WIDTH and HEIGHT must be integers") from exc
    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be strictly positive")

    entry = _parse_coordinates(pairs["ENTRY"], "ENTRY")
    exit_ = _parse_coordinates(pairs["EXIT"], "EXIT")
    perfect = _parse_bool(pairs["PERFECT"], "PERFECT")
    output_file = pairs["OUTPUT_FILE"]

    seed: Optional[int] = None
    if "SEED" in pairs:
        try:
            seed = int(pairs["SEED"])
        except ValueError as exc:
            raise ConfigError("SEED must be an integer") from exc

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit_=exit_,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
