from pathlib import Path

from app.core.scanner_config import ScannerConfig


class RepositoryScanner:

    def __init__(self, config: ScannerConfig | None = None):
        self._config = config or ScannerConfig()

    def scan(self, repository_path: str) -> list[Path]:

        root = Path(repository_path)

        if not root.exists():
            raise FileNotFoundError(
                f"Repository not found: {repository_path}"
            )

        files = []

        for path in root.rglob("*"):

            if not path.is_file():
                continue

            if self._should_ignore(path):
                continue

            files.append(path)

        return sorted(files)

    def _should_ignore(self, path: Path) -> bool:

        if path.suffix.lower() in self._config.ignored_extensions:
            return True

        for part in path.parts:
            if part in self._config.ignored_directories:
                return True

        return False