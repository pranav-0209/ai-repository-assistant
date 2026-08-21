from unittest.mock import Mock

from app.retrieval.repository_retriever import RepositoryRetriever


def test_retrieve_embeds_question_and_returns_code_chunks():
    embedding_service = Mock()
    vector_store = Mock()

    embedding_service.embed.return_value = [
        0.1,
        0.2,
        0.3,
    ]

    vector_store.query.return_value = {
        "documents": [
            [
                "public User registerUser() { ... }",
            ]
        ],
        "metadatas": [
            [
                {
                    "file_path": "services/UserService.java",
                    "language": "Java",
                    "symbol": "registerUser",
                    "symbol_type": "method",
                    "start_line": 10,
                    "end_line": 20,
                }
            ]
        ],
        "distances": [
            [
                0.25,
            ]
        ],
    }

    retriever = RepositoryRetriever(
        embedding_service,
        vector_store,
    )

    results = retriever.retrieve(
        "How are users registered?",
        n_results=3,
    )

    embedding_service.embed.assert_called_once_with(
        "How are users registered?"
    )

    vector_store.query.assert_called_once_with(
        [0.1, 0.2, 0.3],
        n_results=3,
    )

    assert len(results) == 1

    result = results[0]

    assert result.symbol == "registerUser"
    assert result.file_path == "services/UserService.java"
    assert result.language == "Java"
    assert result.symbol_type == "method"
    assert result.start_line == 10
    assert result.end_line == 20
    assert result.distance == 0.25


def test_retrieve_returns_empty_list_for_blank_question():
    embedding_service = Mock()
    vector_store = Mock()

    retriever = RepositoryRetriever(
        embedding_service,
        vector_store,
    )

    results = retriever.retrieve("   ")

    assert results == []

    embedding_service.embed.assert_not_called()
    vector_store.query.assert_not_called()