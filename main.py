from app.indexing.language_detector import LanguageDetector
from app.indexing.metadata_extractor import FileMetadataExtractor
from app.indexing.repository_indexer import RepositoryIndexer
from app.indexing.repository_scanner import RepositoryScanner


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

    repository = indexer.index("repositories")

    print(f"\nRepository: {repository.path}")
    print(f"Files discovered: {len(repository.files)}\n")

    for file in repository.files:
        print(
            f"{file.path} | "
            f"{file.language} | "
            f"{file.size_bytes} bytes | "
            f"{file.line_count} lines"
        )


if __name__ == "__main__":
    main()