# Agent Overview

## Architecture

The autonomous agent is built with a modular architecture consisting of several key components that work together to enable intelligent decision-making and task execution.

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────┐
│  Planning Module│◄────┤Feedback Module│◄────│   Workflows  │
│   (Q-learning)  │     │              │     │              │
└────────┬────────┘     └──────────────┘     └──────┬───────┘
         │                                          │
         │                                         │
         ▼                                         ▼
┌─────────────────┐                        ┌──────────────┐
│  Memory Module  │◄───────────────────────│    Tools     │
│    (Qdrant)     │                        │              │
└─────────────────┘                        └──────────────┘
```

## Core Components

### Planning Module
- Implements Q-learning algorithm for decision making
- Maintains action-value mappings
- Selects optimal actions based on current state
- Located in `src/planning/planning_module.py`

### Memory Module
- Uses Qdrant for vector storage
- Stores action history and results
- Enables context-aware decision making
- Located in `src/memory/memory_module.py`

### Feedback Module
- Evaluates action outcomes
- Updates Q-learning model
- Provides performance metrics
- Located in `src/feedback/feedback_module.py`

### Workflows
- Define task execution patterns
- Implement business logic
- Current workflows:
  - Signal analysis
  - News research
- Located in `src/workflows/`

### Tools
- External service integrations
- Implemented tools:
  - Telegram messaging
  - Twitter interaction
- Planned tools:
  - News API
  - Perplexity research
- Located in `src/tools/`

## Decision Making Process

1. **State Assessment**
   - Agent evaluates current context
   - Retrieves relevant memories
   - Analyzes available actions

2. **Action Selection**
   - Q-learning model selects optimal action
   - Based on historical performance
   - Considers current state

3. **Execution**
   - Selected workflow is triggered
   - Tools are utilized as needed
   - Results are captured

4. **Feedback Loop**
   - Action outcomes are evaluated
   - Q-learning model is updated
   - Memory is stored for future reference

## Configuration

The agent's behavior can be configured through:
- Environment variables
- Configuration files
- Q-learning parameters

For detailed setup instructions, refer to the [README](../../README.md).
