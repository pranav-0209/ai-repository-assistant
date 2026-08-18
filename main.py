from app.indexing.language_detector import LanguageDetector
from app.indexing.metadata_extractor import FileMetadataExtractor
from app.indexing.repository_indexer import RepositoryIndexer
from app.indexing.repository_scanner import RepositoryScanner
from app.indexing.repository_summary import RepositorySummaryService
from app.indexing.repository_summary_formatter import (
    RepositorySummaryFormatter,
)


def main():
    scanner = RepositoryScanner()

    language_detector = LanguageDetector()

    metadata_extractor = FileMetadataExtractor(
        language_detector
    )

    indexer = RepositoryIndexer(
        scanner,
        metadata_extractor,
    )

    repository = indexer.index("repositories/sample_project")

    summary_service = RepositorySummaryService()

    summary = summary_service.summarize(repository)

    formatter = RepositorySummaryFormatter()

    print(formatter.format(repository, summary))


if __name__ == "__main__":
    main()