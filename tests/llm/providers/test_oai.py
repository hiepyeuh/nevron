# from unittest.mock import AsyncMock, MagicMock, patch
# import pytest
# from loguru import logger
# from openai import AsyncOpenAI
# from openai.types.chat import ChatCompletion, ChatCompletionMessage

# from src.core.config import settings
# from src.core.exceptions import LLMError
# from src.llm.providers.oai import call_openai


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
#     monkeypatch.setattr(settings, "OPENAI_API_KEY", "test-key")
#     monkeypatch.setattr(settings, "OPENAI_MODEL", "gpt-4")
#     return settings


# def create_mock_completion(content: str) -> ChatCompletion:
#     """Helper function to create mock ChatCompletion responses."""
#     message = MagicMock(spec=ChatCompletionMessage)
#     message.content = content

#     choice = MagicMock()
#     choice.message = message

#     completion = MagicMock(spec=ChatCompletion)
#     completion.choices = [choice]

#     return completion


# @pytest.fixture
# def mock_openai_client():
#     """Create a mock OpenAI client with chat completions."""
#     with patch("openai.AsyncOpenAI") as mock:
#         client = mock.return_value
#         chat = MagicMock()
#         completions = AsyncMock()
#         completions.create = AsyncMock()
#         chat.completions = completions
#         client.chat = chat

#         # Set up default response
#         mock_response = create_mock_completion("Test response")
#         completions.create.return_value = mock_response

#         return client


# @pytest.mark.asyncio
# async def test_call_openai_basic(mock_openai_client, mock_logger):
#     """Test basic OpenAI API call with simple message."""
#     # arrange:
#     mock_debug, _ = mock_logger
#     messages = [{"role": "user", "content": "Hello"}]

#     # act:
#     response = await call_openai(messages)

#     # assert:
#     mock_openai_client.chat.completions.create.assert_called_once_with(
#         model="gpt-4",
#         messages=messages,
#         temperature=0.2
#     )
#     assert response == "Test response"
#     mock_debug.assert_any_call(
#         f"Calling OpenAI with model=gpt-4, temperature=0.2, messages={messages}"
#     )


# @pytest.mark.asyncio
# async def test_call_openai_with_system_message(mock_openai_client):
#     """Test OpenAI API call with system message."""
#     # arrange:
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "Hello"}
#     ]

#     # act:
#     await call_openai(messages)

#     # assert:
#     mock_openai_client.chat.completions.create.assert_called_once()
#     actual_messages = mock_openai_client.chat.completions.create.call_args[1]["messages"]
#     assert actual_messages == messages


# @pytest.mark.asyncio
# async def test_call_openai_with_conversation(mock_openai_client):
#     """Test OpenAI API call with full conversation."""
#     # arrange:
#     messages = [
#         {"role": "system", "content": "System prompt"},
#         {"role": "user", "content": "Hello"},
#         {"role": "assistant", "content": "Hi there"},
#         {"role": "user", "content": "How are you?"}
#     ]

#     # act:
#     await call_openai(messages)

#     # assert:
#     mock_openai_client.chat.completions.create.assert_called_once()
#     actual_messages = mock_openai_client.chat.completions.create.call_args[1]["messages"]
#     assert actual_messages == messages


# @pytest.mark.asyncio
# async def test_call_openai_with_custom_params(mock_openai_client):
#     """Test OpenAI API call with custom parameters."""
#     # arrange:
#     messages = [{"role": "user", "content": "Hello"}]
#     custom_params = {
#         "model": "gpt-3.5-turbo",
#         "temperature": 0.7
#     }

#     # act:
#     await call_openai(messages, **custom_params)

#     # assert:
#     mock_openai_client.chat.completions.create.assert_called_once()
#     call_kwargs = mock_openai_client.chat.completions.create.call_args[1]
#     assert call_kwargs["model"] == "gpt-3.5-turbo"
#     assert call_kwargs["temperature"] == 0.7


# @pytest.mark.asyncio
# async def test_call_openai_api_error(mock_openai_client, mock_logger):
#     """Test error handling for API failures."""
#     # arrange:
#     messages = [{"role": "user", "content": "Hello"}]
#     error_message = "API Error"
#     mock_openai_client.chat.completions.create.side_effect = Exception(error_message)
#     _, mock_error = mock_logger

#     # act/assert:
#     with pytest.raises(LLMError, match="Error during OpenAI API call"):
#         await call_openai(messages)

#     mock_error.assert_called_once()
#     assert error_message in mock_error.call_args[0][0]


# @pytest.mark.asyncio
# async def test_call_openai_empty_response(mock_openai_client, mock_logger):
#     """Test handling of empty response content."""
#     # arrange:
#     messages = [{"role": "user", "content": "Hello"}]
#     mock_response = create_mock_completion("")  # Empty content
#     mock_openai_client.chat.completions.create.return_value = mock_response
#     _, mock_error = mock_logger

#     # act/assert:
#     with pytest.raises(LLMError, match="No content in OpenAI response"):
#         await call_openai(messages)


# @pytest.mark.asyncio
# async def test_call_openai_response_processing(mock_openai_client, mock_logger):
#     """Test proper processing of API response."""
#     # arrange:
#     mock_debug, _ = mock_logger
#     messages = [{"role": "user", "content": "Hello"}]
#     mock_response = create_mock_completion("  Processed response  \n")  # Add extra whitespace
#     mock_openai_client.chat.completions.create.return_value = mock_response

#     # act:
#     response = await call_openai(messages)

#     # assert:
#     assert response == "Processed response"  # Should be stripped
#     mock_debug.assert_any_call("OpenAI response: Processed response")
