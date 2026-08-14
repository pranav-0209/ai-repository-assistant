from app.indexing.repository_scanner import RepositoryScanner


def main():
    scanner = RepositoryScanner()

    repository_path = "repositories"

    files = scanner.scan(repository_path)

    print(f"\nDiscovered {len(files)} files:\n")

    for file in files:
        print(file)


if __name__ == "__main__":
    main()