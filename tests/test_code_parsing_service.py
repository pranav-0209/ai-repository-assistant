from pathlib import Path

from app.indexing.models import RepositoryFile
from app.parsing.code_parsing_service import CodeParsingService

def test_code_parsing_service_parses_scanner_relative_path(
    tmp_path: Path,
):
    repository_root = tmp_path / "sample_project"
    repository_root.mkdir()

    source_file = repository_root / "UserService.java"

    source_file.write_text(
        """\
public class UserService {

    public void createUser() {
    }
}
""",
        encoding="utf-8",
    )

    repository_file = RepositoryFile(
        path=Path("UserService.java"),
        language="Java",
        size_bytes=source_file.stat().st_size,
        line_count=source_file.read_text(
            encoding="utf-8"
        ).count("\n"),
    )

    service = CodeParsingService()

    result = service.parse_file(
        repository_root,
        repository_file,
    )

    assert result is not None

    classes = [
        symbol
        for symbol in result.symbols
        if symbol.symbol_type == "class"
    ]

    methods = [
        symbol
        for symbol in result.symbols
        if symbol.symbol_type == "method"
    ]

    assert len(classes) == 1
    assert classes[0].name == "UserService"

    assert len(methods) == 1
    assert methods[0].name == "createUser"