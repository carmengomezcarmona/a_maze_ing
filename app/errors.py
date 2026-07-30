"""Custom exceptions raised by the application layer."""


class ConfigError(Exception):
    """Raised when the configuration file is missing, malformed or invalid."""
