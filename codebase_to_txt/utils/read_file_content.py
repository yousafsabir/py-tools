import sys
from pathlib import Path


def read_file_content(file_path: str, base_dir: str = ".") -> str | None:
    """
    Read content from a file.

    Args:
        file_path: Relative path to the file
        base_dir: Base directory to resolve paths from

    Returns:
        File content as string, or None if file doesn't exist
    """
    full_path = Path(base_dir) / file_path

    if not full_path.exists():
        print(f"Warning: File not found: {full_path}", file=sys.stderr)
        return None

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Handle binary files
        print(f"Warning: Skipping binary file: {full_path}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading {full_path}: {e}", file=sys.stderr)
        return None
