# from unittest.mock import AsyncMock, MagicMock, patch
# import pytest
# from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic
# from loguru import logger

# from src.core.config import settings
# from src.core.exceptions import LLMError
# from src.llm.providers.anthropic import call_anthropic


# @pytest.fixture
# def mock_logger(monkeypatch):
#     """Mock logger for testing."""
#     mock_debug = MagicMock()
#     mock_error = MagicMock()
#     monkeypatch.setattr(logger, "debug", mock_debug)
#     monkeypatch.setattr(logger, "error", mock_error)
#     return mock_debug, mock_error


# @pytest.fixture
# def mock_settings(monkeypatch):
#     """Mock settings for testing."""
#     monkeypatch.setattr(settings, "ANTHROPIC_API_KEY", "test-key")
#     monkeypatch.setattr(settings, "ANTHROPIC_MODEL", "claude-2")
#     return settings


# @pytest.fixture
# def mock_anthropic_client():
#     """Create a mock Anthropic client."""
#     with patch("src.llm.providers.anthropic.Anthropic") as mock:
#         client = mock.return_value
#         client.completions.create = AsyncMock()
#         mock_response = MagicMock()
#         mock_response.completion = "Test response"
#         client.completions.create.return_value = mock_response
#         return client


# @pytest.mark.asyncio
# async def test_call_anthropic_basic(mock_anthropic_client, mock_logger):
#     """Test basic Anthropic API call with simple message."""
#     # arrange:
#     messages = [{"role": "user", "content": "Hello"}]
#     expected_prompt = f"{HUMAN_PROMPT} Hello\n\n{AI_PROMPT}"

#     # act:
#     response = await call_anthropic(messages)

#     # assert:
#     mock_anthropic_client.completions.create.assert_called_once_with(
#         prompt=expected_prompt,
#         model="claude-2",
#         temperature=0.7,
#         max_tokens_to_sample=1024
#     )
#     assert response == "Test response"


# @pytest.mark.asyncio
# async def test_call_anthropic_with_system_message(mock_anthropic_client):
#     """Test Anthropic API call with system message."""
#     # arrange:
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "Hello"}
#     ]
#     expected_prompt = (
#         f"(System) You are a helpful assistant\n\n"
#         f"{HUMAN_PROMPT} Hello\n\n{AI_PROMPT}"
#     )

#     # act:
#     await call_anthropic(messages)

#     # assert:
#     mock_anthropic_client.completions.create.assert_called_once()
#     actual_prompt = mock_anthropic_client.completions.create.call_args[1]["prompt"]
#     assert actual_prompt == expected_prompt


# @pytest.mark.asyncio
# async def test_call_anthropic_with_conversation(mock_anthropic_client):
#     """Test Anthropic API call with full conversation."""
#     # arrange:
#     messages = [
#         {"role": "system", "content": "System prompt"},
#         {"role": "user", "content": "Hello"},
#         {"role": "assistant", "content": "Hi there"},
#         {"role": "user", "content": "How are you?"}
#     ]
#     expected_prompt = (
#         f"(System) System prompt\n\n"
#         f"{HUMAN_PROMPT} Hello\n\n"
#         f"{AI_PROMPT} Hi there\n\n"
#         f"{HUMAN_PROMPT} How are you?\n\n"
#         f"{AI_PROMPT}"
#     )

#     # act:
#     await call_anthropic(messages)

#     # assert:
#     mock_anthropic_client.completions.create.assert_called_once()
#     actual_prompt = mock_anthropic_client.completions.create.call_args[1]["prompt"]
#     assert actual_prompt == expected_prompt


# @pytest.mark.asyncio
# async def test_call_anthropic_with_custom_params(mock_anthropic_client):
#     """Test Anthropic API call with custom parameters."""
#     # arrange:
#     messages = [{"role": "user", "content": "Hello"}]
#     custom_params = {
#         "model": "claude-instant-1",
#         "temperature": 0.5
#     }

#     # act:
#     await call_anthropic(messages, **custom_params)

#     # assert:
#     mock_anthropic_client.completions.create.assert_called_once()
#     call_kwargs = mock_anthropic_client.completions.create.call_args[1]
#     assert call_kwargs["model"] == "claude-instant-1"
#     assert call_kwargs["temperature"] == 0.5


# @pytest.mark.asyncio
# async def test_call_anthropic_api_error(mock_anthropic_client, mock_logger):
#     """Test error handling for API failures."""
#     # arrange:
#     messages = [{"role": "user", "content": "Hello"}]
#     error_message = "API Error"
#     mock_anthropic_client.completions.create.side_effect = Exception(error_message)
#     _, mock_error = mock_logger

#     # act/assert:
#     with pytest.raises(LLMError, match="Error during Anthropic API call"):
#         await call_anthropic(messages)

#     mock_error.assert_called_once()
#     assert error_message in mock_error.call_args[0][0]


# @pytest.mark.asyncio
# async def test_call_anthropic_empty_messages(mock_anthropic_client):
#     """Test Anthropic API call with empty messages list."""
#     # arrange:
#     messages = []
#     expected_prompt = AI_PROMPT  # Should only contain the final AI prompt

#     # act:
#     await call_anthropic(messages)

#     # assert:
#     mock_anthropic_client.completions.create.assert_called_once()
#     actual_prompt = mock_anthropic_client.completions.create.call_args[1]["prompt"]
#     assert actual_prompt == expected_prompt


# @pytest.mark.asyncio
# async def test_call_anthropic_response_processing(mock_anthropic_client, mock_logger):
#     """Test proper processing of API response."""
#     # arrange:
#     mock_debug, _ = mock_logger
#     messages = [{"role": "user", "content": "Hello"}]
#     mock_response = MagicMock()
#     mock_response.completion = "  Processed response  \n"  # Add extra whitespace
#     mock_anthropic_client.completions.create.return_value = mock_response

#     # act:
#     response = await call_anthropic(messages)

#     # assert:
#     assert response == "Processed response"  # Should be stripped
#     mock_debug.assert_any_call("Anthropic response: Processed response")
