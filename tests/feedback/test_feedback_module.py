from unittest.mock import MagicMock

import pytest
from loguru import logger

from src.feedback.feedback_module import FeedbackModule


@pytest.fixture
def mock_logger(monkeypatch):
    """Mock logger for testing."""
    mock_debug = MagicMock()
    mock_error = MagicMock()
    monkeypatch.setattr(logger, "debug", mock_debug)
    monkeypatch.setattr(logger, "error", mock_error)
    return mock_debug, mock_error


@pytest.fixture
def feedback_module():
    """Create a FeedbackModule instance."""
    return FeedbackModule()


def test_init():
    """Test FeedbackModule initialization."""
    module = FeedbackModule()
    assert isinstance(module.feedback_history, list)
    assert len(module.feedback_history) == 0


def test_collect_feedback_success(feedback_module, mock_logger):
    """Test feedback collection for successful action."""
    # arrange:
    mock_debug, _ = mock_logger
    action = "test_action"
    outcome = "success"

    # act:
    score = feedback_module.collect_feedback(action, outcome)

    # assert:
    assert score == 0.0  # Currently hardcoded to 0.0 as per DEBUG comment
    assert len(feedback_module.feedback_history) == 1

    entry = feedback_module.feedback_history[0]
    assert entry["action"] == action
    assert entry["outcome"] == outcome
    assert entry["score"] == 0.0
    assert entry["status"] == "neutral"

    mock_debug.assert_any_call(f"Collecting feedback for action '{action}'")
    mock_debug.assert_any_call(f"Feedback recorded: {entry}")


def test_collect_feedback_failure(feedback_module):
    """Test feedback collection for failed action."""
    # arrange:
    action = "test_action"
    outcome = None

    # act:
    score = feedback_module.collect_feedback(action, outcome)

    # assert:
    assert score == 0.0  # Currently hardcoded to 0.0 as per DEBUG comment
    assert len(feedback_module.feedback_history) == 1

    entry = feedback_module.feedback_history[0]
    assert entry["action"] == action
    assert entry["outcome"] is None
    assert entry["score"] == 0.0
    assert entry["status"] == "neutral"


def test_collect_multiple_feedback(feedback_module):
    """Test collecting multiple feedback entries."""
    # arrange:
    actions = ["action1", "action2", "action3"]
    outcomes = ["success", None, "partial"]

    # act:
    scores = [
        feedback_module.collect_feedback(action, outcome)
        for action, outcome in zip(actions, outcomes)
    ]

    # assert:
    assert len(scores) == 3
    assert len(feedback_module.feedback_history) == 3

    for i, (action, outcome) in enumerate(zip(actions, outcomes)):
        entry = feedback_module.feedback_history[i]
        assert entry["action"] == action
        assert entry["outcome"] == outcome
        assert entry["score"] == 0.0  # Currently hardcoded
        assert entry["status"] == "neutral"  # Currently hardcoded


def test_get_feedback_history_empty(feedback_module):
    """Test getting feedback history when empty."""
    history = feedback_module.get_feedback_history()
    assert isinstance(history, list)
    assert len(history) == 0


def test_get_feedback_history_with_limit(feedback_module):
    """Test getting limited feedback history."""
    # arrange:
    # Add 5 feedback entries
    for i in range(5):
        feedback_module.collect_feedback(f"action{i}", f"outcome{i}")

    # act:
    # Get last 3 entries
    history = feedback_module.get_feedback_history(limit=3)

    # assert:
    assert len(history) == 3
    assert history[0]["action"] == "action2"
    assert history[1]["action"] == "action3"
    assert history[2]["action"] == "action4"


def test_get_feedback_history_limit_exceeds_size(feedback_module):
    """Test getting feedback history with limit larger than history size."""
    # arrange:
    feedback_module.collect_feedback("action1", "outcome1")
    feedback_module.collect_feedback("action2", "outcome2")

    # act:
    history = feedback_module.get_feedback_history(limit=5)

    # assert:
    assert len(history) == 2  # Should return all entries


def test_reset_feedback_history(feedback_module, mock_logger):
    """Test resetting feedback history."""
    # arrange:
    mock_debug, _ = mock_logger
    feedback_module.collect_feedback("action1", "outcome1")
    feedback_module.collect_feedback("action2", "outcome2")
    assert len(feedback_module.feedback_history) == 2

    # act:
    feedback_module.reset_feedback_history()

    # assert:
    assert len(feedback_module.feedback_history) == 0
    mock_debug.assert_any_call("Feedback history has been reset.")


@pytest.mark.parametrize(
    "action,outcome",
    [
        ("", None),  # Empty action
        ("action", ""),  # Empty string outcome
        ("action", 123),  # Numeric outcome
        ("action", {"key": "value"}),  # Dict outcome
    ],
)
def test_collect_feedback_different_types(feedback_module, action, outcome):
    """Test feedback collection with different input types."""
    # act:
    score = feedback_module.collect_feedback(action, outcome)

    # assert:
    assert score == 0.0  # Currently hardcoded
    assert len(feedback_module.feedback_history) == 1
    entry = feedback_module.feedback_history[0]
    assert entry["action"] == action
    assert entry["outcome"] == outcome
