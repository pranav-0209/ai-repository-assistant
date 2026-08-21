from app.embeddings.embedding_service import EmbeddingService
from app.retrieval.models import RetrievedCodeChunk
from app.vectorstore.chroma_store import ChromaVectorStore


class RepositoryRetriever:
    """Retrieves repository code relevant to a user question."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: ChromaVectorStore,
    ):
        self._embedding_service = embedding_service
        self._vector_store = vector_store

    def retrieve(
        self,
        question: str,
        n_results: int = 5,
    ) -> list[RetrievedCodeChunk]:
        if not question.strip():
            return []

        query_embedding = self._embedding_service.embed(question)

        results = self._vector_store.query(
            query_embedding,
            n_results=n_results,
        )

        return self._build_results(results)

    @staticmethod
    def _build_results(results) -> list[RetrievedCodeChunk]:
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved_chunks: list[RetrievedCodeChunk] = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            retrieved_chunks.append(
                RetrievedCodeChunk(
                    content=document,
                    file_path=metadata["file_path"],
                    language=metadata["language"],
                    symbol=metadata["symbol"],
                    symbol_type=metadata["symbol_type"],
                    start_line=int(metadata["start_line"]),
                    end_line=int(metadata["end_line"]),
                    distance=float(distance),
                )
            )

        return retrieved_chunks