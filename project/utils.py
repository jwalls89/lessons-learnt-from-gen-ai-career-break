"""Utility functions for cross-platform task operations."""

from pathlib import Path


def ensure_directory(path: str | Path) -> Path:
    """Create a directory and all parent directories if they don't exist.

    This is a cross-platform replacement for `mkdir -p` shell command.

    Args:
        path: Directory path to create (string or Path object)

    Returns:
        Path object of the created directory

    Example:
        >>> ensure_directory(".quality/pipaudit")
        PosixPath('.quality/pipaudit')

    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def get_current_working_directory() -> Path:
    """Get the absolute path of the current working directory.

    This is a cross-platform replacement for `$(pwd)` shell command.

    Returns:
        Absolute Path object of current working directory

    Example:
        >>> get_current_working_directory()
        PosixPath('/home/user/project')

    """
    return Path.cwd().resolve()
