from app.embeddings.embedding_service import EmbeddingService
from app.qa.context_builder import ContextBuilder
from app.qa.repository_qa_service import RepositoryQAService
from app.retrieval.repository_retriever import RepositoryRetriever
from app.vectorstore.chroma_store import ChromaVectorStore


def create_repository_qa_service(
    persist_directory: str = "data/chroma",
) -> RepositoryQAService:
    embedding_service = EmbeddingService()

    vector_store = ChromaVectorStore(
        persist_directory,
    )

    retriever = RepositoryRetriever(
        embedding_service,
        vector_store,
    )

    context_builder = ContextBuilder()

    return RepositoryQAService(
        retriever,
        context_builder,
    )