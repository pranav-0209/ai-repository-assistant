from app.chunking.code_chunking_service import CodeChunkingService
from app.embeddings.embedding_service import EmbeddingService
from app.indexing.repository_indexer import RepositoryIndexer
from app.vectorstore.chroma_store import ChromaVectorStore


class RepositoryVectorIndexer:
    """
    Builds a persistent vector index for a repository.
    """

    def __init__(
        self,
        repository_indexer: RepositoryIndexer,
        chunking_service: CodeChunkingService,
        embedding_service: EmbeddingService,
        vector_store: ChromaVectorStore,
    ):
        self._repository_indexer = repository_indexer
        self._chunking_service = chunking_service
        self._embedding_service = embedding_service
        self._vector_store = vector_store

    def index(self, repository_path: str) -> int:
        repository = self._repository_indexer.index(
            repository_path
        )

        chunks = self._chunking_service.chunk_repository(
            repository
        )

        if not chunks:
            return 0

        embeddings = self._embedding_service.embed_many(
            [chunk.content for chunk in chunks]
        )

        self._vector_store.add_chunks(
            chunks,
            embeddings,
        )

        return len(chunks)