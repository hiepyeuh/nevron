import pytest
from src.feedback.feedback_module import FeedbackModule

# test fixtures
@pytest.fixture
def feedback_module():
    """
    fixture that provides a fresh feedback module instance for each test
    """
    return FeedbackModule()

def test_feedback_module_initialization(feedback_module):
    """
    test that feedback module initializes with empty history
    """
    assert feedback_module.feedback_history == []

def test_collect_feedback_success(feedback_module):
    """
    test collecting feedback for successful action
    """
    action = "test_action"
    outcome = "success_result"
    
    score = feedback_module.collect_feedback(action, outcome)
    
    # currently hardcoded to 0.0 as per debug comment in implementation
    assert score == 0.0
    assert len(feedback_module.feedback_history) == 1
    
    entry = feedback_module.feedback_history[0]
    assert entry["action"] == action
    assert entry["outcome"] == outcome
    assert entry["score"] == 0.0
    assert entry["status"] == "neutral"

def test_collect_feedback_failure(feedback_module):
    """
    test collecting feedback for failed action
    """
    action = "failed_action"
    outcome = None
    
    score = feedback_module.collect_feedback(action, outcome)
    
    # currently hardcoded to 0.0 as per debug comment in implementation
    assert score == 0.0
    assert len(feedback_module.feedback_history) == 1
    
    entry = feedback_module.feedback_history[0]
    assert entry["action"] == action
    assert entry["outcome"] is None
    assert entry["score"] == 0.0
    assert entry["status"] == "neutral"

def test_get_feedback_history_limit(feedback_module):
    """
    test retrieving limited feedback history
    """
    # add multiple feedback entries
    for i in range(15):
        feedback_module.collect_feedback(f"action_{i}", f"outcome_{i}")
    
    # test default limit (10)
    history = feedback_module.get_feedback_history()
    assert len(history) == 10
    
    # test custom limit
    history = feedback_module.get_feedback_history(limit=5)
    assert len(history) == 5
    
    # verify most recent entries are returned
    assert history[-1]["action"] == "action_14"
    assert history[-1]["outcome"] == "outcome_14"

def test_reset_feedback_history(feedback_module):
    """
    test resetting feedback history
    """
    # add some feedback entries
    feedback_module.collect_feedback("test_action", "test_outcome")
    feedback_module.collect_feedback("another_action", "another_outcome")
    
    assert len(feedback_module.feedback_history) == 2
    
    # reset history
    feedback_module.reset_feedback_history()
    assert len(feedback_module.feedback_history) == 0
