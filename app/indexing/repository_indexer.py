from pathlib import Path

from app.indexing.models import Repository, RepositoryFile
from app.indexing.repository_scanner import RepositoryScanner


class RepositoryIndexer:
    """
    Builds a structured representation of a repository.
    """

    def __init__(self, scanner: RepositoryScanner):
        self._scanner = scanner

    def index(self, repository_path: str) -> Repository:
        root = Path(repository_path)

        files = self._scanner.scan(repository_path)

        repository_files = [
            RepositoryFile(path=file)
            for file in files
        ]

        return Repository(
            path=root,
            files=repository_files,
        )