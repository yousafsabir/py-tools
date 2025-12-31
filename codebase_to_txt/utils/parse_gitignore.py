import sys


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
