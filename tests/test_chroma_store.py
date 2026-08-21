from unittest.mock import Mock, patch

from app.chunking.models import CodeChunk
from app.vectorstore.chroma_store import ChromaVectorStore


def test_add_chunks_upserts_embeddings_documents_and_metadata():
    mock_client = Mock()
    mock_collection = Mock()

    mock_client.get_or_create_collection.return_value = (
        mock_collection
    )

    chunk = CodeChunk(
        content="def create_user():\n    pass",
        file_path="services/user_service.py",
        language="Python",
        symbol="create_user",
        symbol_type="function",
        start_line=1,
        end_line=2,
    )

    embeddings = [[0.1, 0.2, 0.3]]

    with patch(
        "app.vectorstore.chroma_store.chromadb.PersistentClient",
        return_value=mock_client,
    ):
        store = ChromaVectorStore("test-data")

        store.add_chunks(
            [chunk],
            embeddings,
        )

    mock_collection.upsert.assert_called_once_with(
        ids=[
            "services/user_service.py:create_user:1:2"
        ],
        embeddings=embeddings,
        documents=[
            "def create_user():\n    pass"
        ],
        metadatas=[
            {
                "file_path": "services/user_service.py",
                "language": "Python",
                "symbol": "create_user",
                "symbol_type": "function",
                "start_line": 1,
                "end_line": 2,
            }
        ],
    )


def test_add_chunks_rejects_mismatched_lengths():
    with patch(
        "app.vectorstore.chroma_store.chromadb.PersistentClient"
    ):
        store = ChromaVectorStore("test-data")

    chunk = CodeChunk(
        content="pass",
        file_path="test.py",
        language="Python",
        symbol="test",
        symbol_type="function",
        start_line=1,
        end_line=1,
    )

    try:
        store.add_chunks(
            [chunk],
            [],
        )
        assert False
    except ValueError as exc:
        assert str(exc) == (
            "Number of chunks must match number of embeddings."
        )