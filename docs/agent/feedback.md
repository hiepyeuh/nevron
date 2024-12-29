# **Feedback Module**

## Overview

The Feedback Module is an integral component designed to collect and process feedback for actions performed by the agent. It enables the system to evaluate outcomes, track performance, and adapt behavior based on historical data. This module is vital for improving the agent's decision-making and maintaining accountability.

The Feedback Module is implemented in `src/feedback/feedback_module.py` and provides structured methods for collecting, storing, and analyzing feedback related to agent actions.

---

## How It Works

The Feedback Module operates as follows:

1. **Feedback Collection**:
   Captures feedback based on the action performed and its outcome, assigning a feedback score to evaluate success or failure.

2. **Feedback Storage**:
   Maintains an internal history of feedback entries, including details about the action, its outcome, and the assigned feedback score.

3. **Feedback Retrieval**:
   Allows querying of recent feedback entries for analysis and monitoring.

4. **Feedback Reset**:
   Provides functionality to clear feedback history, ensuring the module can be reset when needed.

---

## Technical Features

### 1. Feedback Collection

The `collect_feedback` method records feedback for a specific action and its outcome. It assigns a feedback score based on predefined criteria:

- **Failure**: Assigned a score of `-1.0` if the outcome is `None`.
- **Success**: Assigned a score of `1.0` for successful outcomes.

#### Implementation:

```python
feedback_score = -1.0 if outcome is None else 1.0
```

- **Inputs**:

  - `action` (str): The name of the action performed.
  - `outcome` (Any): The outcome of the action; `None` for failure or a value indicating success.

- **Output**:

  - Returns a feedback score (`float`) for the action.

- **Example Usage**:

```python
feedback_score = feedback_module.collect_feedback("fetch_data", outcome=data)
```

---

### 2. Feedback History Retrieval

The `get_feedback_history` method retrieves the most recent feedback entries, limited by the specified count.

#### Features:

- Enables monitoring of agent performance.
- Default limit is set to 10 entries.

#### Example:

```python
recent_feedback = feedback_module.get_feedback_history(limit=5)
```

---

### 3. Feedback Reset

The `reset_feedback_history` method clears the internal feedback history, resetting the module's state. This is useful for testing or reinitializing feedback tracking.

#### Example:

```python
feedback_module.reset_feedback_history()
```

---

## Key Methods

### `collect_feedback`

Captures feedback for a given action and outcome.

**Arguments**:

- `action` (str): The action name.
- `outcome` (Optional[Any]): The outcome of the action.

**Returns**:

- `float`: Feedback score.

### `get_feedback_history`

Retrieves recent feedback entries.

**Arguments**:

- `limit` (int): Number of entries to retrieve (default: 10).

**Returns**:

- `List[Dict[str, Any]]`: Recent feedback entries.

### `reset_feedback_history`

Clears the feedback history.

**Returns**:

- `None`

---

## Example Workflow

1. An action is performed by the agent (e.g., `fetch_data`).
2. The outcome of the action is evaluated, and feedback is collected:
   ```python
   feedback_module.collect_feedback("fetch_data", outcome=data)
   ```
3. The collected feedback is stored in the feedback history for analysis.
4. The feedback history can be retrieved for review:
   ```python
   recent_feedback = feedback_module.get_feedback_history(limit=5)
   ```
5. Feedback history is reset when needed:
   ```python
   feedback_module.reset_feedback_history()
   ```

---

## Benefits

- **Performance Monitoring**: Tracks agent actions and their outcomes, enabling better performance evaluation.
- **Adaptability**: Facilitates improvements by learning from historical data.
- **Simplicity**: Provides clear and structured methods for feedback collection and retrieval.

---

## Best Practices

1. **Consistent Feedback Collection**: Ensure feedback is collected for all critical actions to build a comprehensive history.
2. **Periodic Reset**: Use `reset_feedback_history` to clear stale feedback during testing or major updates.
3. **Logging**: Leverage `loguru` for detailed insights into feedback processing.

---

## Known Limitations

- **Scoring Granularity**: Feedback scores are currently binary (`-1.0` or `1.0`). Future versions can introduce more nuanced scoring.
- **Debugging Notes**: Debugging comments in `collect_feedback` indicate areas for improvement.

---

If you have any questions or need further assistance, please refer to the [GitHub Discussions](https://github.com/axioma-ai-labs/nevron/discussions).

