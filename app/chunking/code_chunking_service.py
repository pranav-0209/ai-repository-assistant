from app.chunking.code_chunker import CodeChunker
from app.chunking.models import CodeChunk
from app.indexing.models import Repository


class CodeChunkingService:
    """
    Creates code-aware chunks for an entire repository.
    """

    def __init__(self, code_chunker: CodeChunker):
        self._code_chunker = code_chunker

    def chunk_repository(
        self,
        repository: Repository,
    ) -> list[CodeChunk]:
        chunks: list[CodeChunk] = []

        for repository_file in repository.files:
            chunks.extend(
                self._code_chunker.chunk(repository_file)
            )

        return chunks