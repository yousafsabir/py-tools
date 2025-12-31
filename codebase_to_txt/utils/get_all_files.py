import os
from pathlib import Path

from utils.parse_gitignore import parse_gitignore
from utils.should_ignore_path import should_ignore_path


def get_all_files(
    directory: str,
    recursive: bool = True,
    sort: bool = False,
    additional_ignore: list[str] | None = None,
    use_gitignore: bool = True,
) -> list[str]:
    """
    Get all file paths in a directory.

    Args:
        directory: Root directory to search
        recursive: Whether to search subdirectories
        sort: Whether to sort the file paths
        additional_ignore: Additional directories and files to ignore
        use_gitignore: Whether to parse and use .gitignore file if present

    Returns:
        List of file paths relative to the directory
    """
    ignore_patterns = [
        ".env",
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
        ".next",
        "public",
    ]

    # Parse .gitignore if it exists and use_gitignore is True
    if use_gitignore:
        gitignore_path = Path(directory) / ".gitignore"
        if gitignore_path.exists():
            gitignore_patterns = parse_gitignore(str(gitignore_path))
            if gitignore_patterns:
                print(f"Loaded {len(gitignore_patterns)} pattern(s) from .gitignore")
                ignore_patterns.extend(gitignore_patterns)

    # Extend with additional ignore patterns if provided
    if additional_ignore:
        ignore_patterns.extend(additional_ignore)

    file_paths: list[str] = []
    directory_path = Path(directory)

    if recursive:
        for root, dirs, files in os.walk(directory):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_patterns]

            for file in files:
                file_path = Path(root) / file
                # Get relative path from the base directory
                relative_path = file_path.relative_to(directory_path)

                # Check if file should be ignored
                if not should_ignore_path(relative_path, ignore_patterns):
                    file_paths.append(str(relative_path))
    else:
        for item in directory_path.iterdir():
            if item.is_file():
                relative_path = item.relative_to(directory_path)
                if not should_ignore_path(relative_path, ignore_patterns):
                    file_paths.append(item.name)

    if sort:
        file_paths = sorted(file_paths)

    return file_paths
