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

        repository_files: list[RepositoryFile] = []

        for path in paths:
            repository_file = self._metadata_extractor.extract(path)

            parsed_code = self.code_parsing_service.parse_file(
                root,
                repository_file,
            )

            repository_file = RepositoryFile(
                path=repository_file.path,
                language=repository_file.language,
                size_bytes=repository_file.size_bytes,
                line_count=repository_file.line_count,
                parsed_code=parsed_code,
            )

            repository_files.append(repository_file)

        return Repository(
            path=root,
            files=repository_files,
        )