from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from loguru import logger

from src.workflows.research_news import analyze_news_workflow


@pytest.fixture
def mock_workflow_logger(monkeypatch):
    """Mock logger for workflow testing."""
    mock_info = MagicMock()
    mock_error = MagicMock()
    monkeypatch.setattr(logger, "info", mock_info)
    monkeypatch.setattr(logger, "error", mock_error)
    return mock_info, mock_error


@pytest.fixture
def mock_memory():
    """Create a mock memory module."""
    memory = MagicMock()
    memory.search = AsyncMock()
    memory.store = AsyncMock()
    return memory


@pytest.mark.asyncio
async def test_analyze_news_success(mock_workflow_logger, mock_memory):
    """Test successful news analysis and tweet posting."""
    # arrange:
    mock_info, mock_error = mock_workflow_logger
    news_content = "Test news content"
    tweet_text = "Breaking News:\nTest analysis\n#StayInformed"
    tweet_id = "123456789"

    # Mock memory search for context
    mock_memory.search.return_value = [
        {"event": "event1", "outcome": "outcome1"},
        {"event": "event2", "outcome": "outcome2"},
    ]

    # Mock LLM
    mock_llm = AsyncMock()
    mock_llm.generate_response = AsyncMock(return_value="Test analysis")

    # Mock Twitter post
    mock_post = AsyncMock(return_value=[tweet_id])

    with (
        patch("src.workflows.research_news.LLM", return_value=mock_llm),
        patch("src.workflows.research_news.post_twitter_thread", mock_post),
    ):
        # act:
        result = await analyze_news_workflow(news_content, memory=mock_memory)

    # assert:
    assert result == tweet_id
    mock_memory.search.assert_called_once_with("recent events", top_k=3)
    mock_llm.generate_response.assert_called_once()
    mock_post.assert_called_once_with(tweets={"tweet1": tweet_text})
    mock_info.assert_any_call("Analyzing news...")
    mock_info.assert_any_call(f"Publishing tweet:\n{tweet_text}")
    mock_info.assert_any_call("Tweet posted successfully!")
    mock_error.assert_not_called()


@pytest.mark.asyncio
async def test_analyze_news_no_context(mock_workflow_logger, mock_memory):
    """Test news analysis when no context is available."""
    # arrange:
    mock_info, mock_error = mock_workflow_logger
    news_content = "Test news content"
    tweet_text = "Breaking News:\nTest analysis\n#StayInformed"
    tweet_id = "123456789"

    # Mock memory search (no context available)
    mock_memory.search.return_value = []

    # Mock LLM
    mock_llm = AsyncMock()
    mock_llm.generate_response = AsyncMock(return_value="Test analysis")

    # Mock Twitter post
    mock_post = AsyncMock(return_value=[tweet_id])

    with (
        patch("src.workflows.research_news.LLM", return_value=mock_llm),
        patch("src.workflows.research_news.post_twitter_thread", mock_post),
    ):
        # act:
        result = await analyze_news_workflow(news_content, memory=mock_memory)

    # assert:
    assert result == tweet_id
    mock_memory.search.assert_called_once_with("recent events", top_k=3)
    mock_llm.generate_response.assert_called_once()
    mock_post.assert_called_once_with(tweets={"tweet1": tweet_text})
    mock_info.assert_any_call("Analyzing news...")
    mock_error.assert_not_called()


@pytest.mark.asyncio
async def test_analyze_news_llm_error(mock_workflow_logger, mock_memory):
    """Test error handling when LLM fails."""
    # arrange:
    mock_info, mock_error = mock_workflow_logger
    news_content = "Test news content"

    # Mock memory search
    mock_memory.search.return_value = [{"event": "event1", "outcome": "outcome1"}]

    # Mock LLM with error
    mock_llm = AsyncMock()
    mock_llm.generate_response = AsyncMock(side_effect=Exception("LLM error"))

    with patch("src.workflows.research_news.LLM", return_value=mock_llm):
        # act:
        result = await analyze_news_workflow(news_content, memory=mock_memory)

    # assert:
    assert result is None
    mock_memory.search.assert_called_once()
    mock_llm.generate_response.assert_called_once()
    mock_error.assert_called_once_with("Error in analyze_news_workflow: LLM error")


@pytest.mark.asyncio
async def test_analyze_news_twitter_error(mock_workflow_logger, mock_memory):
    """Test error handling when Twitter posting fails."""
    # arrange:
    mock_info, mock_error = mock_workflow_logger
    news_content = "Test news content"

    # Mock memory search
    mock_memory.search.return_value = [{"event": "event1", "outcome": "outcome1"}]

    # Mock LLM
    mock_llm = AsyncMock()
    mock_llm.generate_response = AsyncMock(return_value="Test analysis")

    # Mock Twitter post with error
    mock_post = AsyncMock(side_effect=Exception("Twitter error"))

    with (
        patch("src.workflows.research_news.LLM", return_value=mock_llm),
        patch("src.workflows.research_news.post_twitter_thread", mock_post),
    ):
        # act:
        result = await analyze_news_workflow(news_content, memory=mock_memory)

    # assert:
    assert result is None
    mock_memory.search.assert_called_once()
    mock_llm.generate_response.assert_called_once()
    mock_post.assert_called_once()
    mock_error.assert_called_once_with("Error in analyze_news_workflow: Twitter error")
