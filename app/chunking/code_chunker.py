from app.chunking.models import CodeChunk
from app.indexing.models import RepositoryFile


class CodeChunker:
    """Converts parsed repository files into code-aware chunks."""

    def chunk(self, repository_file: RepositoryFile) -> list[CodeChunk]:
        parsed_code = repository_file.parsed_code

        if parsed_code is None:
            return []

        source_code = repository_file.path.read_text(
            encoding="utf-8"
        )

        lines = source_code.splitlines()

        chunks: list[CodeChunk] = []

        for symbol in parsed_code.symbols:
            content = self._extract_symbol(
                lines,
                symbol.line_start,
                symbol.line_end,
            )

            if not content.strip():
                continue

            chunks.append(
                CodeChunk(
                    content=content,
                    file_path=str(repository_file.path),
                    language=repository_file.language,
                    symbol=symbol.name,
                    symbol_type=symbol.symbol_type,
                    start_line=symbol.line_start,
                    end_line=symbol.line_end,
                )
            )

        return chunks

    @staticmethod
    def _extract_symbol(
        lines: list[str],
        line_start: int,
        line_end: int,
    ) -> str:
        return "\n".join(
            lines[line_start - 1:line_end]
        )