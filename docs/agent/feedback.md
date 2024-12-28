# Feedback Module

The Feedback Module is a critical component of Nevron's architecture that tracks & evaluates the performance of the AI agent actions through a systematic feedback collection mechanism.

## Overview

The feedback system provides a way to:
- Track success/failure of agent actions
- Maintain a history of action outcomes
- Generate quantitative feedback scores
- Enable performance analysis and optimization

## Implementation

The feedback functionality is implemented in the `FeedbackModule` class located in `src/feedback/feedback_module.py`.

### Key Components

1. **Feedback History**
   - Maintains a list of feedback entries
   - Each entry contains action details, outcomes, and scores
   - Accessible via `get_feedback_history()` method

2. **Feedback Collection**
   - Method: `collect_feedback(action, outcome)`
   - Generates feedback scores based on action outcomes:
     - Success: +1.0
     - Failure: -1.0 
     - Neutral: 0.0
   - Records detailed feedback entries including:
     - Action name
     - Outcome details
     - Numerical score
     - Status (success/failure)

3. **History Management**
   - Retrieve recent feedback via `get_feedback_history(limit)`
   - Reset history using `reset_feedback_history()`
   - Default history limit: 10 entries