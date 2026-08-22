from app.retrieval.models import RetrievedCodeChunk


class ContextBuilder:
    """Builds LLM context from retrieved repository code."""

    def build(
        self,
        chunks: list[RetrievedCodeChunk],
    ) -> str:
        if not chunks:
            return ""

        sections: list[str] = []

        for chunk in chunks:
            sections.append(
                "\n".join(
                    [
                        f"FILE: {chunk.file_path}",
                        f"LANGUAGE: {chunk.language}",
                        f"SYMBOL: {chunk.symbol}",
                        f"TYPE: {chunk.symbol_type}",
                        f"LINES: {chunk.start_line}-{chunk.end_line}",
                        "",
                        chunk.content,
                    ]
                )
            )

        return "\n\n---\n\n".join(sections)