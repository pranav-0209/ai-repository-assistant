from unittest.mock import Mock

from app.chunking.models import CodeChunk
from app.indexing.models import Repository
from app.indexing.repository_vector_indexer import (
    RepositoryVectorIndexer,
)


def test_indexes_repository_chunks():
    repository_indexer = Mock()

    chunking_service = Mock()

    embedding_service = Mock()

    vector_store = Mock()

    repository = Repository(
        path="sample",
        files=[],
    )

    chunks = [
        CodeChunk(
            content="def create_user():\n    pass",
            file_path="user_service.py",
            language="Python",
            symbol="create_user",
            symbol_type="function",
            start_line=1,
            end_line=2,
        )
    ]

    embeddings = [
        [0.1, 0.2, 0.3]
    ]

    repository_indexer.index.return_value = repository

    chunking_service.chunk_repository.return_value = (
        chunks
    )

    embedding_service.embed_many.return_value = (
        embeddings
    )

    indexer = RepositoryVectorIndexer(
        repository_indexer,
        chunking_service,
        embedding_service,
        vector_store,
    )

    result = indexer.index("repositories/sample_project")

    assert result == 1

    repository_indexer.index.assert_called_once_with(
        "repositories/sample_project"
    )

    chunking_service.chunk_repository.assert_called_once_with(
        repository
    )

    embedding_service.embed_many.assert_called_once_with(
        ["def create_user():\n    pass"]
    )

    vector_store.add_chunks.assert_called_once_with(
        chunks,
        embeddings,
    )