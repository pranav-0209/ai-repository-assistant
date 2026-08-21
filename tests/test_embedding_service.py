from unittest.mock import Mock, patch

from app.embeddings.embedding_service import EmbeddingService


def test_embed_returns_single_embedding():
    mock_response = Mock()
    mock_response.embeddings = [
        [0.1, 0.2, 0.3]
    ]

    mock_ollama = Mock()
    mock_ollama.embed.return_value = mock_response

    with patch(
        "app.embeddings.embedding_service.ollama",
        mock_ollama,
    ):
        service = EmbeddingService()

        result = service.embed(
            "create user"
        )

    assert result == [0.1, 0.2, 0.3]

    mock_ollama.embed.assert_called_once_with(
        model="nomic-embed-text",
        input="create user",
    )


def test_embed_many_returns_multiple_embeddings():
    mock_response = Mock()
    mock_response.embeddings = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    mock_ollama = Mock()
    mock_ollama.embed.return_value = mock_response

    with patch(
        "app.embeddings.embedding_service.ollama",
        mock_ollama,
    ):
        service = EmbeddingService()

        result = service.embed_many(
            [
                "create user",
                "delete user",
            ]
        )

    assert result == [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    mock_ollama.embed.assert_called_once_with(
        model="nomic-embed-text",
        input=[
            "create user",
            "delete user",
        ],
    )


def test_embed_many_returns_empty_list_for_empty_input():
    mock_ollama = Mock()

    with patch(
        "app.embeddings.embedding_service.ollama",
        mock_ollama,
    ):
        service = EmbeddingService()

        result = service.embed_many([])

    assert result == []

    mock_ollama.embed.assert_not_called()