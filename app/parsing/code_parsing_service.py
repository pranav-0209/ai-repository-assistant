from pathlib import Path

from app.indexing.models import ParsedCode, RepositoryFile
from app.parsing.parser_factory import CodeParserFactory


class CodeParsingService:

    def parse_file(
        self,
        repository_root: Path,
        repository_file: RepositoryFile,
    ) -> ParsedCode | None:

        parser = CodeParserFactory.create(
            repository_file.language
        )

        if parser is None:
            return None

        if repository_file.path.is_absolute():
            source_path = repository_file.path
        elif repository_file.path.exists():
            source_path = repository_file.path
        else:
            source_path = repository_root / repository_file.path

        try:
            source_code = source_path.read_text(
                encoding="utf-8"
            )

            return parser.parse(source_code)

        except (
            OSError,
            UnicodeDecodeError,
            SyntaxError,
        ):
            return None