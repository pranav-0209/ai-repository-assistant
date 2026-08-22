from app.chunking.code_chunker import CodeChunker
from app.chunking.code_chunking_service import (
    CodeChunkingService,
)
from app.embeddings.embedding_service import EmbeddingService
from app.indexing.language_detector import LanguageDetector
from app.indexing.metadata_extractor import FileMetadataExtractor
from app.indexing.repository_indexer import RepositoryIndexer
from app.indexing.repository_scanner import RepositoryScanner
from app.indexing.repository_vector_indexer import (
    RepositoryVectorIndexer,
)
from app.parsing.code_parsing_service import CodeParsingService
from app.qa.qa_factory import create_repository_qa_service
from app.vectorstore.chroma_store import ChromaVectorStore


REPOSITORY_PATH = "repositories/sample_project"
CHROMA_PATH = "data/chroma"


def create_vector_indexer() -> RepositoryVectorIndexer:
    scanner = RepositoryScanner()

    language_detector = LanguageDetector()

    metadata_extractor = FileMetadataExtractor(
        language_detector
    )

    code_parsing_service = CodeParsingService()

    repository_indexer = RepositoryIndexer(
        scanner,
        metadata_extractor,
        code_parsing_service,
    )

    chunking_service = CodeChunkingService(
        CodeChunker()
    )

    embedding_service = EmbeddingService()

    vector_store = ChromaVectorStore(
        CHROMA_PATH
    )

    return RepositoryVectorIndexer(
        repository_indexer,
        chunking_service,
        embedding_service,
        vector_store,
    )


def main():
    print("Indexing repository...")

    vector_indexer = create_vector_indexer()

    chunk_count = vector_indexer.index(
        REPOSITORY_PATH
    )

    print(
        f"Indexed {chunk_count} code chunks."
    )

    qa_service = create_repository_qa_service(
        CHROMA_PATH
    )

    print()
    print("Repository Assistant is ready.")
    print("Type 'exit' to quit.")
    print()

    while True:
        question = input("Question: ").strip()

        if question.lower() == "exit":
            print("Goodbye.")
            break

        if not question:
            continue

        print()
        print("Answer:")
        print(qa_service.answer(question))
        print()


if __name__ == "__main__":
    main()