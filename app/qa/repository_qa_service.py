import ollama

from app.qa.context_builder import ContextBuilder
from app.retrieval.repository_retriever import RepositoryRetriever


class RepositoryQAService:
    """Answers repository questions using retrieved code context."""

    MODEL_NAME = "qwen2.5-coder:3b"

    def __init__(
        self,
        retriever: RepositoryRetriever,
        context_builder: ContextBuilder,
    ):
        self._retriever = retriever
        self._context_builder = context_builder

    def answer(
        self,
        question: str,
        n_results: int = 5,
    ) -> str:
        chunks = self._retriever.retrieve(
            question,
            n_results=n_results,
        )

        if not chunks:
            return (
                "I could not find relevant code in the repository "
                "to answer this question."
            )

        context = self._context_builder.build(chunks)

        prompt = self._build_prompt(
            question,
            context,
        )

        response = ollama.chat(
            model=self.MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant that answers questions "
                        "about software repositories. "
                        "Use only the provided repository context. "
                        "Do not invent files, classes, methods, or behavior. "
                        "If the context does not contain enough information "
                        "to answer the question, say so clearly."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response.message.content

    @staticmethod
    def _build_prompt(
        question: str,
        context: str,
    ) -> str:
        return f"""Answer the following question about the repository.

QUESTION:
{question}

REPOSITORY CONTEXT:
{context}

INSTRUCTIONS:
- Base your answer on the provided repository context.
- Mention relevant file names and symbols when useful.
- Explain the execution flow when the question asks how something works.
- Do not invent information that is not present in the context.
- If the context is insufficient, explicitly say what information is missing.
"""