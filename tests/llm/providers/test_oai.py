from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core.exceptions import LLMError
from src.llm.providers.oai import call_openai


@pytest.mark.asyncio
async def test_call_openai_success():
    """Test a successful call to OpenAI."""
    mock_message = MagicMock()
    mock_message.content = "This is a mock response from OpenAI."

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    # Mock the AsyncOpenAI client and its `chat.completions.create` method
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value = mock_response

    # Patch the AsyncOpenAI client constructor to return the mock client
    with patch("src.llm.providers.oai.openai.AsyncOpenAI", return_value=mock_client):
        messages = [{"role": "user", "content": "Test message"}]
        result = await call_openai(messages, model="gpt-4", temperature=0.7)

        assert result == "This is a mock response from OpenAI."
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
        )


@pytest.mark.asyncio
async def test_call_openai_no_content():
    """Test when OpenAI returns no content in the response."""
    mock_message = MagicMock()
    mock_message.content = ""

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("src.llm.providers.oai.openai.AsyncOpenAI", return_value=mock_client):
        messages = [{"role": "user", "content": "Test message"}]

        with pytest.raises(LLMError):
            await call_openai(messages)


@pytest.mark.asyncio
async def test_call_openai_exception():
    """Test when OpenAI raises an exception."""
    mock_client = AsyncMock()
    mock_client.chat.completions.create.side_effect = Exception("API call failed")

    with patch("src.llm.providers.oai.openai.AsyncOpenAI", return_value=mock_client):
        messages = [{"role": "user", "content": "Test message"}]

        with pytest.raises(LLMError, match="Error during OpenAI API call"):
            await call_openai(messages)
