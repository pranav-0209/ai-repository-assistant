from pathlib import Path

from app.indexing.models import RepositoryFile
from app.parsing.code_parsing_service import CodeParsingService


def test_code_parsing_service_parses_python_file(tmp_path: Path):
    source_file = tmp_path / "user_service.py"

    source_file.write_text(
        """
class UserService:

    def create_user(self):
        pass
""",
        encoding="utf-8",
    )

    repository_file = RepositoryFile(
        path=Path("user_service.py"),
        language="Python",
        size_bytes=source_file.stat().st_size,
        line_count=source_file.read_text(encoding="utf-8").count("\n"),
    )

    service = CodeParsingService()

    result = service.parse_file(
        tmp_path,
        repository_file,
    )

    assert result is not None
    assert len(result.symbols) == 2

    assert result.symbols[0].name == "UserService"
    assert result.symbols[0].symbol_type == "class"

    assert result.symbols[1].name == "create_user"
    assert result.symbols[1].symbol_type == "method"
    assert result.symbols[1].parent == "UserService"


def test_code_parsing_service_returns_none_for_unsupported_language(
    tmp_path: Path,
):
    source_file = tmp_path / "UserService.java"

    source_file.write_text(
        """
public class UserService {
}
""",
        encoding="utf-8",
    )

    repository_file = RepositoryFile(
        path=Path("UserService.java"),
        language="Java",
        size_bytes=source_file.stat().st_size,
        line_count=source_file.read_text(encoding="utf-8").count("\n"),
    )

    service = CodeParsingService()

    result = service.parse_file(
        tmp_path,
        repository_file,
    )

    assert result is None


def test_code_parsing_service_handles_invalid_python(
    tmp_path: Path,
):
    source_file = tmp_path / "invalid.py"

    source_file.write_text(
        """
def broken(
""",
        encoding="utf-8",
    )

    repository_file = RepositoryFile(
        path=Path("invalid.py"),
        language="Python",
        size_bytes=source_file.stat().st_size,
        line_count=source_file.read_text(encoding="utf-8").count("\n"),
    )

    service = CodeParsingService()

    result = service.parse_file(
        tmp_path,
        repository_file,
    )

    assert result is None