from pathlib import Path

from app.chunking.code_chunker import CodeChunker
from app.indexing.models import ParsedCode, ParsedSymbol, RepositoryFile


def test_chunks_parsed_symbols(tmp_path: Path):
    source = """\
class UserService:
    def create_user(self, user):
        return user
"""

    file_path = tmp_path / "user_service.py"
    file_path.write_text(source, encoding="utf-8")

    parsed_code = ParsedCode(
        symbols=[
            ParsedSymbol(
                name="UserService",
                symbol_type="class",
                line_start=1,
                line_end=3,
            ),
            ParsedSymbol(
                name="create_user",
                symbol_type="method",
                line_start=2,
                line_end=3,
                parent="UserService",
            ),
        ]
    )

    repository_file = RepositoryFile(
        path=file_path,
        language="Python",
        size_bytes=len(source.encode("utf-8")),
        line_count=3,
        parsed_code=parsed_code,
    )

    chunks = CodeChunker().chunk(repository_file)

    assert len(chunks) == 2

    assert chunks[0].symbol == "UserService"
    assert chunks[0].symbol_type == "class"
    assert chunks[0].start_line == 1
    assert chunks[0].end_line == 3
    assert chunks[0].content == (
    "class UserService:\n"
    "    def create_user(self, user):\n"
    "        return user"
)

    assert chunks[1].symbol == "create_user"
    assert chunks[1].symbol_type == "method"
    assert chunks[1].start_line == 2
    assert chunks[1].end_line == 3
    assert chunks[1].content == (
        "    def create_user(self, user):\n"
        "        return user"
    )


def test_returns_empty_list_when_file_is_not_parsed(tmp_path: Path):
    file_path = tmp_path / "README.md"
    file_path.write_text("# README", encoding="utf-8")

    repository_file = RepositoryFile(
        path=file_path,
        language="Markdown",
        size_bytes=8,
        line_count=1,
        parsed_code=None,
    )

    chunks = CodeChunker().chunk(repository_file)

    assert chunks == []