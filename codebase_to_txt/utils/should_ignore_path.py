from pathlib import Path


def should_ignore_path(path: Path, ignore_patterns: list[str]) -> bool:
    """
    Check if a path should be ignored based on patterns.

    Args:
        path: Path to check (relative path)
        ignore_patterns: List of ignore patterns

    Returns:
        True if path should be ignored, False otherwise
    """
    path_str = str(path)
    path_parts = path.parts

    for pattern in ignore_patterns:
        # Check if pattern matches filename
        if path.name == pattern:
            return True

        # Check if pattern matches any directory in path
        if pattern in path_parts:
            return True

        # Handle extension patterns like *.pyc
        if pattern.startswith("*."):
            ext = pattern[1:]  # includes the dot
            if path_str.endswith(ext):
                return True

        # Check if pattern is in the path string
        if pattern in path_str:
            return True

    return False
