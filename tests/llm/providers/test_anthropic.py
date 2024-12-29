from unittest.mock import MagicMock, patch

import pytest

from src.core.exceptions import LLMError
from src.llm.providers.anthropic import call_anthropic


@pytest.mark.asyncio
async def test_call_anthropic_success():
    """Test a successful call to the Anthropic Claude API."""
    mock_response = MagicMock()
    mock_response.completion = "This is a mock response from Anthropic."

    # Mock the Anthropic client and its `completions.create` method
    mock_client = MagicMock()
    mock_client.completions.create.return_value = mock_response

    with patch("src.llm.providers.anthropic.Anthropic", return_value=mock_client):
        messages = [{"role": "user", "content": "Test message"}]
        result = await call_anthropic(messages, model="claude-2", temperature=0.5)

        assert result == "This is a mock response from Anthropic."
        mock_client.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_call_anthropic_no_content():
    """Test when Anthropic returns no content in the response."""
    mock_response = MagicMock()
    mock_response.completion = ""

    mock_client = MagicMock()
    mock_client.completions.create.return_value = mock_response

    with patch("src.llm.providers.anthropic.Anthropic", return_value=mock_client):
        messages = [{"role": "user", "content": "Test message"}]
        await call_anthropic(messages)


@pytest.mark.asyncio
async def test_call_anthropic_exception():
    """Test when Anthropic raises an exception."""
    mock_client = MagicMock()
    mock_client.completions.create.side_effect = Exception("API call failed")

    with patch("src.llm.providers.anthropic.Anthropic", return_value=mock_client):
        messages = [{"role": "user", "content": "Test message"}]

        with pytest.raises(LLMError, match="Error during Anthropic API call"):
            await call_anthropic(messages)
