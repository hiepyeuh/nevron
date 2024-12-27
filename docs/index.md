# Developer Documentation

Learn how to build your first autonomous AI agent with Neurobro's **Autonomous Agent Framework** in Python.

This framework is designed to be a modular and extensible framework for building autonomous AI agents, which can perform tasks idependently on their own.

Follow this guide to learn how to create your first AI agent.

## Overview

The Autonomous AI Agent is an open-source framework that support the development, deployment and management of autonomous AI agents.

This framework is built on top of:

- [Q-learning](https://en.wikipedia.org/wiki/Q-learning) based decision making
- LLM-powered intelligence
- Modular architecture with planning, feedback, and memory components
- Integration with external services (Telegram, Twitter, Discord, etc.)
- Vector-based memory storage using [Qdrant](https://qdrant.tech/)

-----

## 💎 Core Features

- **Autonomous Decision Making**: Autonomous agents uses Q-learning algorithm for intelligent decision making
- **LLM Integration**: Powered by OpenAI & Anthropic Large Language Models
- **Modular Workflows**: Predefined autonomous agent task execution patterns
    - Analyze signal workflow
    - Research news workflow
- **Memory Management**: Qdrant-based vector storage for context retention
- **External Integrations**:
    - Telegram messaging
    - Twitter interaction
    - News API integration (in progress)
    - Perplexity research integration (in progress)

-----

## 🧠 Core Components

### Planning Module
Handles decision-making using Q-learning algorithm to determine optimal actions for the agent.

- **Q-Learning**
  - Uses state-action value mapping for decision making
  - Configurable parameters:
    - Learning rate (PLANNING_ALPHA)
    - Discount factor (PLANNING_GAMMA) 
    - Exploration rate (PLANNING_EPSILON)

-----

### Memory Module
Manages agent's memory using vector storage for efficient context retrieval, which enables the agent to remember and recall previous interactions and events.

- **Multiple Vector Databases Support**
    - Qdrant (primary vector database)
    - Chroma (alternative vector database)

- **Features**
    - Vector embeddings via OpenAI's text-embedding-3-small model
    - Semantic similarity search
    - Metadata storage for context
    - Configurable collection management

- **Backend**
    - Abstract memory backend interface
    - Modular backend architecture for optimal performance & customization
    - Async storage and retrieval operations

-----


### Feedback Module
Feedback module is responsible for processing action results and updating the Q-learning model for improved decision making.

- **Core Functions**
  - Collects feedback from action execution
  - Evaluates action outcomes
  - Updates Q-learning parameters
  - Maintains feedback history

- **Integration**
  - Direct integration with Planning Module
  - Performance metrics tracking

-----

### Tools
Autonomous Agent supports integrations with external services and APIs for extended functionality & integrations in diferent platforms.

Autnomous Agent currently supports the following integrations:

- **Telegram**
    - Bot integration
    - Channel/group support
    - Message formatting

- **Twitter**
    - Tweet posting
    - Media handling
    - Thread creation

- **Research**
    - Perplexity API integration (in progress)
    - News API integration (in progress)

-----

### LLM Integration
Powers the agent's intelligence and natural language capabilities.

- **Supported Providers**
  - OpenAI (primary)
    - GPT-4 for decision making
    - text-embedding-3-small for embeddings
  - Anthropic (alternative)
    - Claude models support
- **Features**
  - Context management
  - Token optimization
  - Response processing

## Getting Started

For setup and development instructions, please refer to our [Quickstart](quickstart.md) file.

## Technical Requirements

- Python 3.12
- Docker (for Qdrant Vector Database)
- Various API keys for integrations:

```
ENVIRONMENT=production

# OpenAI
OPENAI_API_KEY=

# Perplexity
PERPLEXITY_API_KEY=

# Telegram
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Twitter
TWITTER_BEARER_TOKEN=
TWITTER_API_KEY=
TWITTER_API_SECRET_KEY=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=

# Agent
AGENT_PERSONALITY=
AGENT_GOAL=
AGENT_REST_TIME=
```


## Next Steps

- [Quick Start](quickstart.md) → Learn how to create & setup your first autonomous agent
- [Agent](agent/overview.md) → Learn all about Autonomous Agent Framework
- [FAQ](faq.md) → Find answers to your the common questions