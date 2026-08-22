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
                        "You are a repository code analysis assistant. "
                        "Your job is to explain what is actually present in the "
                        "provided repository context.\n\n"
                        "STRICT GROUNDING RULES:\n"
                        "1. Use only information explicitly supported by the "
                        "provided repository context.\n"
                        "2. Never invent files, classes, methods, database queries, "
                        "APIs, frameworks, or behavior.\n"
                        "3. Never assume that a method does something merely because "
                        "that behavior is common in software development.\n"
                        "4. Do not provide hypothetical implementations unless the "
                        "user explicitly asks for one.\n"
                        "5. If the requested functionality is not present in the "
                        "provided context, say that the repository context does not "
                        "contain enough information to answer it.\n"
                        "6. When explaining behavior, distinguish clearly between "
                        "what the code explicitly does and what cannot be determined "
                        "from the provided context.\n"
                        "7. Prefer a concise, factual answer over a speculative one."
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
        return f"""Analyze the repository context below and answer the question.

    QUESTION:
    {question}

    REPOSITORY CONTEXT:
    {context}

    REQUIRED BEHAVIOR:
    - Answer only from the code shown in the repository context.
    - Do not use general programming knowledge to fill missing details.
    - Do not assume that common architecture or framework behavior exists.
    - Do not invent database queries or implementation details.
    - If the requested functionality is not demonstrated by the context,
    explicitly say that it is not present or cannot be determined.
    - Mention the relevant file and symbol when making a claim.
    - If the context only partially answers the question, clearly state
    what can and cannot be determined.

    Return a factual repository-grounded answer.
    """
