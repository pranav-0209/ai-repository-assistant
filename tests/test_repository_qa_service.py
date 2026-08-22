from unittest.mock import Mock, patch

from app.qa.context_builder import ContextBuilder
from app.qa.repository_qa_service import RepositoryQAService
from app.retrieval.models import RetrievedCodeChunk


def test_answer_retrieves_context_and_calls_llm():
    retriever = Mock()

    retriever.retrieve.return_value = [
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

    context_builder = ContextBuilder()

    fake_response = Mock()
    fake_response.message.content = (
        "User registration is handled by UserService.registerUser."
    )

    with patch(
        "app.qa.repository_qa_service.ollama.chat",
        return_value=fake_response,
    ) as mock_chat:

        service = RepositoryQAService(
            retriever,
            context_builder,
        )

        answer = service.answer(
            "How are users registered?"
        )

    assert answer == (
        "User registration is handled by UserService.registerUser."
    )

    retriever.retrieve.assert_called_once_with(
        "How are users registered?",
        n_results=5,
    )

    mock_chat.assert_called_once()

    call_kwargs = mock_chat.call_args.kwargs

    assert call_kwargs["model"] == "qwen2.5-coder:3b"

    messages = call_kwargs["messages"]

    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"

    assert "How are users registered?" in messages[1]["content"]
    assert "UserService.java" in messages[1]["content"]
    assert "registerUser" in messages[1]["content"]


def test_answer_returns_message_when_no_relevant_code_exists():
    retriever = Mock()
    retriever.retrieve.return_value = []

    context_builder = ContextBuilder()

    service = RepositoryQAService(
        retriever,
        context_builder,
    )

    answer = service.answer(
        "How does payment processing work?"
    )

    assert answer == (
        "I could not find relevant code in the repository "
        "to answer this question."
    )