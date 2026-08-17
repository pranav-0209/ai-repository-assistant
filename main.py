from app.indexing.repository_indexer import RepositoryIndexer
from app.indexing.repository_scanner import RepositoryScanner


def main():
    scanner = RepositoryScanner()
    indexer = RepositoryIndexer(scanner)

    repository = indexer.index("repositories")

    print(f"\nRepository: {repository.path}")
    print(f"Files discovered: {len(repository.files)}\n")

    for file in repository.files:
        print(f"{file.name} ({file.extension})")


if __name__ == "__main__":
    main()