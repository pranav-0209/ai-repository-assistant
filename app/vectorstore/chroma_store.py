from pathlib import Path

import chromadb

from app.chunking.models import CodeChunk


class ChromaVectorStore:
    """
    Persistent vector store for repository code chunks.
    """

    COLLECTION_NAME = "repository_code"

    def __init__(self, persist_directory: str = "data/chroma"):
        self._persist_directory = Path(persist_directory)

        self._client = chromadb.PersistentClient(
            path=str(self._persist_directory)
        )

        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )

    def add_chunks(
        self,
        chunks: list[CodeChunk],
        embeddings: list[list[float]],
    ) -> None:

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings."
            )

        if not chunks:
            return

        ids = [
            self._build_id(chunk)
            for chunk in chunks
        ]

        documents = [
            chunk.content
            for chunk in chunks
        ]

        metadatas = [
            {
                "file_path": chunk.file_path,
                "language": chunk.language,
                "symbol": chunk.symbol,
                "symbol_type": chunk.symbol_type,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
            }
            for chunk in chunks
        ]

        self._collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query(
        self,
        embedding: list[float],
        n_results: int = 5,
    ):
        return self._collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
        )

    @staticmethod
    def _build_id(chunk: CodeChunk) -> str:
        return (
            f"{chunk.file_path}:"
            f"{chunk.symbol}:"
            f"{chunk.start_line}:"
            f"{chunk.end_line}"
        )