from pathlib import Path


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
