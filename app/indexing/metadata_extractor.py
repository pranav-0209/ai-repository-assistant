from pathlib import Path

from app.indexing.language_detector import LanguageDetector
from app.indexing.models import RepositoryFile


class FileMetadataExtractor:
    """
    Extracts metadata from repository files.
    """

    def __init__(self, language_detector: LanguageDetector):
        self._language_detector = language_detector

    def extract(self, path: Path) -> RepositoryFile:
        """
        Extract metadata for a single file.
        """

        size_bytes = path.stat().st_size
        line_count = self._count_lines(path)
        language = self._language_detector.detect(path)

        return RepositoryFile(
            path=path,
            language=language,
            size_bytes=size_bytes,
            line_count=line_count,
        )

    def _count_lines(self, path: Path) -> int:
        """
        Count the number of lines in a text file.
        """

        try:
            with path.open(
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as file:
                return sum(1 for _ in file)

        except OSError:
            return 0