from pathlib import Path

from app.indexing.metadata_extractor import FileMetadataExtractor
from app.indexing.models import Repository, RepositoryFile
from app.indexing.repository_scanner import RepositoryScanner


class RepositoryIndexer:
    """
    Builds a structured representation of a repository.
    """

    def __init__(
        self,
        scanner: RepositoryScanner,
        metadata_extractor: FileMetadataExtractor,
        code_parsing_service,
    ):
        self._scanner = scanner
        self._metadata_extractor = metadata_extractor
        self.code_parsing_service = code_parsing_service

    def index(self, repository_path: str) -> Repository:
        root = Path(repository_path)

        paths = self._scanner.scan(repository_path)

        repository_files = [
            self._metadata_extractor.extract(path)
            for path in paths
        ]

        return Repository(
            path=root,
            files=repository_files,
        )