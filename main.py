from app.chunking.code_chunker import CodeChunker
from app.chunking.code_chunking_service import (
    CodeChunkingService,
)
from app.embeddings.embedding_service import EmbeddingService
from app.indexing.language_detector import LanguageDetector
from app.indexing.metadata_extractor import FileMetadataExtractor
from app.indexing.repository_indexer import RepositoryIndexer
from app.indexing.repository_scanner import RepositoryScanner
from app.parsing.code_parsing_service import CodeParsingService
from app.vectorstore.chroma_store import ChromaVectorStore
from app.indexing.repository_vector_indexer import (
    RepositoryVectorIndexer,
)


def main():
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
        "data/chroma"
    )

    vector_indexer = RepositoryVectorIndexer(
        repository_indexer,
        chunking_service,
        embedding_service,
        vector_store,
    )

    chunk_count = vector_indexer.index(
        "repositories/sample_project"
    )

    print(
        f"Indexed {chunk_count} code chunks."
    )


if __name__ == "__main__":
    main()