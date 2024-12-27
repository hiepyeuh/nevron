# Nevron Overview

## Architecture

Nevron is an autonomous AI agent built with a modular architecture consisting of several key components that work together to enable intelligent decision-making and task execution.

![Architecture Diagram](/assets/architecture.png)

### 1. Planning Module (Q-Learning)
The Planning Module serves as the decision-making engine, leveraging [Q-Learning](https://en.wikipedia.org/wiki/Q-learning), a model-free reinforcement learning algorithm. It determines intelligent actions based on the current system state and optimal action planning through learned patterns. The module continuously adapts to new data via feedback loops while maintaining state-action value mappings for consistency.

### 2. Feedback Module
The Feedback Module bridges planning and execution by processing the outcomes of system actions. It evaluates the outcomes of the actions and updates the Q-learning model to improve decision-making.

### 3. Workflows
Workflows act as the execution layer, translating high-level plans into actionable steps. This module manages task sequences and dependencies. It provides standardized operation patterns, maintaining consistency and efficiency throughout the system.

Using workflows, Nevron can perform tasks such as **signal analysis** or *news research*.

### 4. Tools
The Tools module represents the operational toolkit, executing workflow tasks via integrations. It interfaces seamlessly with external services and APIs to deliver concrete implementation capabilities. 

This enables effective real-world interactions such as sending messages to **Telegram** or **Twitter**.

### 5. Memory Module (Qdrant)
The Memory Module, powered by [Qdrant](https://qdrant.tech/), serves as a sophisticated vector storage system for the platform. 

It maintains a persistent history of states and actions, facilitating efficient context retrieval. By storing rewards and learning patterns, it optimizes performance through Qdrant’s advanced vector database capabilities.

-----

## Decision Making Process

1. **State Assessment**
      - Nevron evaluates current context
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

The agent's behavior can be configured via:

- Environment variables
- Configuration files
- Q-learning parameters
- Workflows
- Tools
