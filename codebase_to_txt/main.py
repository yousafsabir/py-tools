#!/usr/bin/env python3
"""
Script to list all file paths in a directory and write them to a file.
"""

import os
import sys
from pathlib import Path
from argparse import ArgumentParser


def get_all_files(
    directory: str, recursive: bool = True, sort: bool = False
) -> list[str]:
    """
    Get all file paths in a directory.

    Args:
        directory: Root directory to search
        recursive: Whether to search subdirectories
        ignore_patterns: List of patterns to ignore (e.g., ['node_modules', '.git'])

    Returns:
        List of file paths relative to the directory
    """
    ignore_patterns = [
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
    ]

    file_paths: list[str] = []
    directory = os.path.join(directory, "src")
    directory_path = Path(directory)

    if recursive:
        for root, dirs, files in os.walk(directory):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_patterns]

            for file in files:
                file_path = Path(root) / file
                # Get relative path from the base directory
                relative_path = file_path.relative_to(directory_path)
                file_paths.append(str(relative_path))
    else:
        for item in directory_path.iterdir():
            if item.is_file():
                file_paths.append(item.name)

    for i in range(len(file_paths)):
        file_paths[i] = "src/" + file_paths[i]

    if sort:
        file_paths = sorted(file_paths)

    return file_paths


def get_language_from_extension(file_path: str):
    """
    Map file extension to syntax highlighting language.

    Args:
        file_path: Path to the file

    Returns:
        Language identifier for syntax highlighting
    """
    ext = Path(file_path).suffix[1:]  # Remove the dot

    lang_map = {
        "ts": "typescript",
        "tsx": "tsx",
        "js": "javascript",
        "jsx": "jsx",
        "json": "json",
        "py": "python",
        "yml": "yaml",
        "yaml": "yaml",
        "md": "markdown",
        "html": "html",
        "css": "css",
        "scss": "scss",
        "sass": "sass",
        "sh": "bash",
        "bash": "bash",
        "sql": "sql",
        "env": "bash",
        "xml": "xml",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
        "h": "c",
        "go": "go",
        "rs": "rust",
        "php": "php",
        "rb": "ruby",
        "swift": "swift",
        "kt": "kotlin",
        "r": "r",
        "dart": "dart",
    }

    return lang_map.get(ext, "")


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


def generate_documentation(
    codebase_dir_path: str, output_file: str | None = None
):
    """
    Generate documentation with code blocks of a codebase.

    Args:
        codebase_dir_path: Base directory where source files are located
        output_file: Output documentation file. If not provided, it will be generated based on the codebase directory name.
    """
    if not os.path.exists(codebase_dir_path):
        print(
            f"Error: Codebase directory not found: {codebase_dir_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    if not output_file:
        codebase_dir = os.path.split(codebase_dir_path)
        output_file = os.path.join(codebase_dir[0], codebase_dir[1] + ".txt")

    file_paths = get_all_files(directory=codebase_dir_path, recursive=True)

    print(f"Processing {len(file_paths)} file(s)...")

    successful = 0
    skipped = 0

    # Generate documentation
    with open(output_file, "w", encoding="utf-8") as out:
        for file_path in file_paths:
            print(f"Processing: {file_path}")

            # Read file content
            content = read_file_content(file_path, codebase_dir_path)

            if content is None:
                skipped += 1
                continue

            # Get language for syntax highlighting
            lang = get_language_from_extension(file_path)

            # Write to output
            out.write(f"{file_path}\n")
            out.write(f"```{lang}\n")
            out.write(content)
            # Ensure content ends with newline before closing backticks
            if content and not content.endswith("\n"):
                out.write("\n")
            out.write("```\n\n")

            successful += 1

    print("\nSummary:")
    print(f"  Processed: {successful} file(s)")
    print(f"  Skipped: {skipped} file(s)")
    print(f"  Output written to: {output_file}")


def main():
    args = ArgumentParser()
    args.add_argument("--codebase", "-c", help="Codebase directory path")
    args.add_argument("--output", "-o", help="Output file")
    args = args.parse_args()
    if not args.codebase:
        print("Error: Codebase directory path is required.")
        sys.exit(1)

    generate_documentation(
        codebase_dir_path=args.codebase, output_file=args.output
    )


if __name__ == "__main__":
    main()
