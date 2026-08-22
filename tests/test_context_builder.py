from app.qa.context_builder import ContextBuilder
from app.retrieval.models import RetrievedCodeChunk


def test_context_builder_includes_code_metadata_and_content():
    chunks = [
        RetrievedCodeChunk(
            content="return userRepository.save(user);",
            file_path="services/UserService.java",
            language="Java",
            symbol="registerUser",
            symbol_type="method",
            start_line=10,
            end_line=15,
            distance=0.2,
        )
    ]

    builder = ContextBuilder()

    context = builder.build(chunks)

    assert "FILE: services/UserService.java" in context
    assert "LANGUAGE: Java" in context
    assert "SYMBOL: registerUser" in context
    assert "TYPE: method" in context
    assert "LINES: 10-15" in context
    assert "return userRepository.save(user);" in context


def test_context_builder_returns_empty_string_for_no_chunks():
    builder = ContextBuilder()

    assert builder.build([]) == ""