import ollama


class EmbeddingService:
    """
    Generates text embeddings using an Ollama embedding model.
    """

    MODEL_NAME = "nomic-embed-text"

    def embed(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text input.
        """

        response = ollama.embed(
            model=self.MODEL_NAME,
            input=text,
        )

        return response.embeddings[0]

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple text inputs.
        """

        if not texts:
            return []

        response = ollama.embed(
            model=self.MODEL_NAME,
            input=texts,
        )

        return response.embeddings