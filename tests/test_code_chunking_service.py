from pathlib import Path

from app.chunking.code_chunker import CodeChunker
from app.chunking.code_chunking_service import CodeChunkingService
from app.indexing.models import (
    ParsedCode,
    ParsedSymbol,
    Repository,
    RepositoryFile,
)


def test_chunks_all_parsed_repository_files(
    tmp_path: Path,
):
    user_service = tmp_path / "UserService.java"
    user_service.write_text(
        """\
public class UserService {

    public void createUser() {
    }
}
""",
        encoding="utf-8",
    )

    auth_service = tmp_path / "AuthService.java"
    auth_service.write_text(
        """\
public class AuthService {

    public void login() {
    }
}
""",
        encoding="utf-8",
    )

    repository = Repository(
        path=tmp_path,
        files=[
            RepositoryFile(
                path=user_service,
                language="Java",
                size_bytes=user_service.stat().st_size,
                line_count=5,
                parsed_code=ParsedCode(
                    symbols=[
                        ParsedSymbol(
                            name="UserService",
                            symbol_type="class",
                            line_start=1,
                            line_end=5,
                        ),
                        ParsedSymbol(
                            name="createUser",
                            symbol_type="method",
                            line_start=3,
                            line_end=4,
                            parent="UserService",
                        ),
                    ]
                ),
            ),
            RepositoryFile(
                path=auth_service,
                language="Java",
                size_bytes=auth_service.stat().st_size,
                line_count=5,
                parsed_code=ParsedCode(
                    symbols=[
                        ParsedSymbol(
                            name="AuthService",
                            symbol_type="class",
                            line_start=1,
                            line_end=5,
                        ),
                        ParsedSymbol(
                            name="login",
                            symbol_type="method",
                            line_start=3,
                            line_end=4,
                            parent="AuthService",
                        ),
                    ]
                ),
            ),
        ],
    )

    service = CodeChunkingService(
        CodeChunker()
    )

    chunks = service.chunk_repository(repository)

    assert len(chunks) == 4

    assert [chunk.symbol for chunk in chunks] == [
        "UserService",
        "createUser",
        "AuthService",
        "login",
    ]