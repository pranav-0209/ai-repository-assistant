from unittest.mock import patch

from app.embeddings.embedding_service import EmbeddingService


def test_embedding_manual_smoke():
    with patch("app.embeddings.embedding_service.ollama.embed") as mock_embed:
        mock_embed.return_value.embeddings = [[0.1, 0.2, 0.3, 0.4, 0.5]]

        service = EmbeddingService()
        embedding = service.embed("public void createUser() {}")

    assert isinstance(embedding, list)
    assert len(embedding) == 5
    print("Embedding dimensions:", len(embedding))
    print("First 10 values:", embedding[:10])


if __name__ == "__main__":
    service = EmbeddingService()
    embedding = service.embed("public void createUser() {}")
    print("Embedding dimensions:", len(embedding))
    print("First 10 values:", embedding[:10])
