#!/usr/bin/env python3
"""
Script to list all file paths in a directory and write them to a file.
"""

import os
import sys
from argparse import ArgumentParser
from pathlib import Path


def parse_gitignore(gitignore_path: str) -> list[str]:
    """
    Parse a .gitignore file and return list of patterns.

    Args:
        gitignore_path: Path to the .gitignore file

    Returns:
        List of patterns to ignore
    """
    patterns = []

    try:
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line in f:
                # Strip whitespace
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Skip negation patterns (lines starting with !)
                # These would require more complex logic to handle properly
                if line.startswith("!"):
                    continue

                # Remove trailing slashes (directory markers)
                # We treat both files and directories the same for our purposes
                if line.endswith("/"):
                    line = line.rstrip("/")

                # Handle leading slashes (match from root only)
                # For simplicity, we'll strip them and match anywhere
                if line.startswith("/"):
                    line = line.lstrip("/")

                # Skip patterns with wildcards for now
                # You can enhance this to handle glob patterns if needed
                # For basic use, we'll only add simple directory/file names
                if "*" not in line and "?" not in line and "[" not in line:
                    patterns.append(line)
                else:
                    # For wildcard patterns, extract meaningful parts
                    # e.g., "*.pyc" -> "pyc" pattern matching
                    # This is a simplified approach
                    if line.startswith("*."):
                        # Extension pattern like *.pyc, *.log
                        patterns.append(line)
                    elif "/" not in line:
                        # Simple wildcard pattern without path separators
                        patterns.append(line)

    except Exception as e:
        print(f"Warning: Could not parse .gitignore: {e}", file=sys.stderr)

    return patterns


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
    codebase_dir_path: str,
    output_file: str | None = None,
    omit_dirs: list[str] | None = None,
    use_gitignore: bool = True,
):
    """
    Generate documentation with code blocks of a codebase.

    Args:
        codebase_dir_path: Base directory where source files are located
        output_file: Output documentation file. If not provided, it will be generated based on the codebase directory name.
        omit_dirs: Additional directories and files to ignore
        use_gitignore: Whether to parse and use .gitignore file if present
    """
    if not os.path.exists(codebase_dir_path):
        print(
            f"Error: Codebase directory not found: {codebase_dir_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    codebase_dir_path = os.path.abspath(codebase_dir_path)

    if not output_file:
        output_file = os.path.join(
            codebase_dir_path, os.path.split(codebase_dir_path)[1] + ".txt"
        )

    file_paths = get_all_files(
        directory=codebase_dir_path,
        recursive=True,
        additional_ignore=omit_dirs,
        use_gitignore=use_gitignore,
    )

    print(f"Processing {len(file_paths)} file(s)...")
    if omit_dirs:
        print(f"Additional omitted patterns: {', '.join(omit_dirs)}")

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
            _ = out.write(f"{file_path}\n")
            _ = out.write(f"```{lang}\n")
            _ = out.write(content)
            # Ensure content ends with newline before closing backticks
            if content and not content.endswith("\n"):
                _ = out.write("\n")
            _ = out.write("```\n\n")

            successful += 1

    print("\nSummary:")
    print(f"  Processed: {successful} file(s)")
    print(f"  Skipped: {skipped} file(s)")
    print(f"  Output written to: {output_file}")


def main():
    args = ArgumentParser()
    args.add_argument("-r", "--result", help="Output file")
    args.add_argument("-c", "--codebase", help="Codebase directory path")
    args.add_argument(
        "-o",
        "--omit",
        help="Comma-separated list of directories/files to ignore (e.g., '.cache,tmp,.env')",
    )
    args.add_argument(
        "--no-gitignore",
        action="store_true",
        help="Disable .gitignore parsing",
    )
    args.add_argument("result_pos", nargs="?", help="Output file (positional)")
    args = args.parse_args()

    # Use -r flag if provided, otherwise fall back to positional
    output_file = args.result or args.result_pos

    args.codebase = args.codebase or os.getcwd()

    # Parse comma-separated omit directories
    omit_dirs = None
    if args.omit:
        omit_dirs = [d.strip() for d in args.omit.split(",")]

    generate_documentation(
        codebase_dir_path=args.codebase,
        output_file=output_file,
        omit_dirs=omit_dirs,
        use_gitignore=not args.no_gitignore,
    )


if __name__ == "__main__":
    main()
