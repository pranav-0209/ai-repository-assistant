from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScannerConfig:
    """
    Configuration for repository scanning.
    """

    ignored_directories: set[str] = field(default_factory=lambda: {
        ".git",
        ".idea",
        ".vscode",
        "node_modules",
        "venv",
        "__pycache__",
        "build",
        "dist",
        "target",
        ".pytest_cache",
    })

    ignored_extensions: set[str] = field(default_factory=lambda: {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".ico",
        ".pdf",
        ".zip",
        ".jar",
        ".exe",
        ".dll",
        ".class",
        ".pyc",
    })