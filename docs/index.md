# Welcome to Autonomous Agent Documentation

This documentation provides a comprehensive guide to the autonomous agent system that uses Q-learning for decision making and integrates with various external services.

## Overview

The autonomous agent is designed to perform tasks independently using a combination of:

- Q-learning based decision making
- OpenAI LLM-powered intelligence
- Modular architecture with planning, feedback, and memory components
- Integration with external services (Telegram, Twitter)
- Vector-based memory storage using Qdrant

## Core Features

- **Autonomous Decision Making**: Uses Q-learning algorithm for intelligent decision making
- **LLM Integration**: Powered by OpenAI language models
- **Modular Workflows**: Predefined task execution patterns
  - Analyze signal workflow
  - Research news workflow
- **Memory Management**: Qdrant-based vector storage for context retention
- **External Integrations**:
  - Telegram messaging
  - Twitter interaction
  - News API integration (planned)
  - Perplexity research integration (planned)

## Core Components

### Planning Module
Handles decision-making using Q-learning algorithms to determine optimal actions.

### Memory Module
Manages agent's memory using Qdrant vector storage for efficient context retrieval.

### Feedback Module
Processes action results and updates the Q-learning model for improved decision making.

### Tools
Provides integrations with external services and APIs for extended functionality.

## Getting Started

For setup and development instructions, please refer to our [README](../README.md) file.

## Technical Requirements

- Python 3.12
- Docker (for Qdrant)
- Various API keys for external services

## Documentation Sections

- [Agent Overview](agent/overview.md)
- [LLM Integration](agent/llm.md)
- [Workflows](agent/workflows.md)