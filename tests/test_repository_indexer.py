from pathlib import Path

from app.indexing.language_detector import LanguageDetector
from app.indexing.metadata_extractor import FileMetadataExtractor
from app.indexing.repository_indexer import RepositoryIndexer
from app.indexing.repository_scanner import RepositoryScanner
from app.parsing.code_parsing_service import CodeParsingService


def test_repository_indexer_parses_supported_files(
    tmp_path: Path,
):
    source_file = tmp_path / "UserService.java"

    source_file.write_text(
        """\
public class UserService {

    public void createUser() {
    }
}
""",
        encoding="utf-8",
    )

    scanner = RepositoryScanner()

    metadata_extractor = FileMetadataExtractor(
        LanguageDetector()
    )

    indexer = RepositoryIndexer(
        scanner,
        metadata_extractor,
        CodeParsingService(),
    )

    repository = indexer.index(str(tmp_path))

    assert len(repository.files) == 1

    repository_file = repository.files[0]

    assert repository_file.path == source_file
    assert repository_file.language == "Java"

    assert repository_file.parsed_code is not None

    classes = [
        symbol
        for symbol in repository_file.parsed_code.symbols
        if symbol.symbol_type == "class"
    ]

    methods = [
        symbol
        for symbol in repository_file.parsed_code.symbols
        if symbol.symbol_type == "method"
    ]

    assert len(classes) == 1
    assert classes[0].name == "UserService"

    assert len(methods) == 1
    assert methods[0].name == "createUser"