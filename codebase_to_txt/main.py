#!/usr/bin/env python3
"""
Script to list all file paths in a directory and write them to a file.
"""

import os
import sys
from argparse import ArgumentParser

from utils.get_all_files import get_all_files
from utils.get_language_from_extension import get_language_from_extension
from utils.read_file_content import read_file_content


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
