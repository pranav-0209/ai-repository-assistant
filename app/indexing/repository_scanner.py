from pathlib import Path

class RepositoryScanner:
    """
    Responsible for discovering all files inside a repository.
    """

    def scan(self, repository_path: str) -> list[Path]:
        """
        Recursively scans a repository and returns all files.

        Args:
            repository_path: Path to the repository.

        Returns:
            List of file paths.
        """

        root = Path(repository_path)

        if not root.exists():
            raise FileNotFoundError(
                f"Repository not found: {repository_path}"
            )

        files = []

        for path in root.rglob("*"):
            if path.is_file():
                files.append(path)

        return sorted(files)