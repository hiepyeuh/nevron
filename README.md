# Autonomous Agent
[![CI](https://github.com/axioma-ai-labs/aa-core/actions/workflows/main.yml/badge.svg)](https://github.com/axioma-ai-labs/aa-core/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/axioma-ai-labs/aa-core/graph/badge.svg?token=krO46pgB7P)](https://codecov.io/gh/axioma-ai-labs/aa-core)

## Table of Contents

- [Overview](#overview)
- [Code structure](#code-structure)
- [Prebuilt tech features](#prebuilt-tech-features)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

This is a simple autonomous agent which can perform various tasks on its own.

Description of the agent in bullet points:
- This autonomous agent is designed to perform the tasks on his own. 
- The core of the agent is implemented by planning, feedback and memory modules. 
- The real intelligence is powered by LLMs. Currently we support OpenAI and Anthropic.
- The actions of the agent are defined in workflows, which encapsulate logic of performing the task.
- Different 3rd party services are integrated with the agent via tools, which are used in the workflows. Example of the tools:
  - Telegram
  - Twitter
  - Perplexity for research
  - Some API for getting news (to be customized)

Some more details about some modules:

### Planning module

The planning module is responsible for making decisions and planning the next action. It uses the Q-learning algorithm to make decisions. The details can be found in code at the [planning_module.py](src/planning/planning_module.py) file.

### Feedback module

The feedback module is responsible for providing feedback to the agent and updating the Q-learning model (in Planning module). It uses the feedback from the previous action, such as the result of the action and type of the action, to evaluate the result of the action and give this result to the Planning module (to update the Q-learning model). The details can be found in code at the [feedback_module.py](src/feedback/feedback_module.py) file.

### Memory module

The memory module is responsible for storing the memories of the agent: what actions were performed, what was the result of the action, etc. Currently we provide Chroma and Qdrant as a memory backend. The details can be found in code at the [memory_module.py](src/memory/memory_module.py) file.  

### Workflows

The workflows are responsible for stating "actions" to the agent. The details can be found in code at the [workflows](src/workflows) folder. This is the place where you define what actually the agent will perform. Currently, we implement the following workflows:

- Analyze signal
- Research news

See the code for more details.

## Code structure

The code can be found in the [src](src) folder.

Overview of the `src` folder:

- [main.py](src/main.py) - the main entry point of the agent
- [agent.py](src/agent.py) - the definition of the agent
- [core](src/core) - the core of the project, which defines settings, definitions and exceptions
- [memory](src/memory) - the memory module
- [planning](src/planning) - the planning module
- [feedback](src/feedback) - the feedback module
- [tools](src/tools) - the tools module
- [llm](src/llm) - the logic of interacting with LLMs
- [workflows](src/workflows) - the workflows

## Prebuilt tech Features

### 1. Pyenv, Pipenv and Docker

The project uses Pyenv for managing Python versions and Pipenv for managing dependencies. Find more details in the [Development](#development) section. Also we need to have Docker installed for running the Qdrant container. Install this software first (follow the official documentation).

### 2. Pydantic

The project uses `Pydantic` for data validation and settings management. Is relatively simple and easy to use.

### 3. Ruff, Isort, Mypy

The project uses `Ruff` for formatting, `Isort` for sorting imports, and `Mypy` for static typing. 
Recommended to use with `Makefile` commands. For more information look at the 
[Makefile](./Makefile).

### 4. Github Actions

The project uses Github Actions for CI/CD. Look at the [.github/workflows](.github/workflows) for 
more information. The package includes the linting workflow per default.

### 5. Makefile

The project uses Makefile for automating tasks. Look at the [Makefile](./Makefile) for more 
information.

The provided Makefile includes the following commands:

```
make deps    # Install dependencies
make format  # Format code
make lint    # Lint code
make run     # Run the agent
```

## Development

### Pyenv and Pipenv

You will need to have Python 3.12 and pipenv installed. The next step is to checkout the repository 
and install the Python dependencies. Then, you will be able to utilize the CLI and run the tests. 
The following assumes a Debian/Ubuntu machine; your mileage may vary.

### Docker (optional)

If you want to use Qdrant as a memory backend, you need to have Docker installed for running the Qdrant container. Install this software first (follow the official documentation).

### Quickstart

Follow these steps to get the project running.

#### Install Dependencies

You can use the provided Makefile files to install the dependencies.

```
make deps
```

Alternatively, you can install the dependencies manually:

```
pipenv install --dev
```

#### Setup Environment Variables

You can use the provided `.env.dev` file to find the environment variables you might want to set up.

```
cp .env.dev .env
```

> [!NOTE]
> You must set the `OPENAI_API_KEY` environment variable to run the agent. The embeddings for the memory module are powered by OpenAI.

> [!NOTE]
> If you want to use Perplexity for research (news analysis workflow), you need to set the `PERPLEXITY_API_KEY` environment variable.

### Run the Agent

Run the agent:

```bash
make run
```

Alternatively, you can run the agent manually:

```bash
pipenv run python -m src.main
```

#### Run the Agent with Qdrant

If you want to use Qdrant as a memory backend, you need to have Docker installed for running the Qdrant container.

Create the `qdrant_storage` folder for running the Qdrant docker container.

```bash
mkdir qdrant_storage
```

Run the Qdrant docker container. (First pull the image with `docker pull qdrant/qdrant`)

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

### Configuration

There are settings you can configure for the agent. To do so, you can edit the `.env` file. 

Here is the list of the settings you can configure:

#### General settings

- `ENVIRONMENT` - the environment in which the agent is running ("production", "development", "ci")
- `PROJECT_NAME` - the name of the project. Typically the name of your agent.
- `PERSISTENT_Q_TABLE_PATH` - the path to the persistent Q-table file for the planning module.
- `PLANNING_ALPHA` - the learning rate for the planning module. Increase for faster adaptation but risk instability. Decrease for more stable but slower learning.
- `PLANNING_GAMMA` - the discount factor for the planning module. Set closer to 1 for long-term planning. Set lower (e.g., 0.5) for short-term rewards.
- `PLANNING_EPSILON` - the exploration rate for the planning module. Increase to encourage exploration in unpredictable environments. Decrease for environments where optimal actions are well-known.
- `MEMORY_BACKEND_TYPE` - the type of the memory backend ("chroma", "qdrant")
- `MEMORY_COLLECTION_NAME` - the name of the memory collection
- `MEMORY_HOST` - the host of the memory backend. This is used only for Qdrant.
- `MEMORY_PORT` - the port of the memory backend. This is used only for Qdrant.
- `MEMORY_VECTOR_SIZE` - the vector size of the memory backend. This is used only for Qdrant. Chroma uses automatically calculated vector size.
- `MEMORY_PERSIST_DIRECTORY` - the directory to persist the memory backend. This is used only for Chroma.
- `LLM_PROVIDER` - the type of the LLM provider ("openai", "anthropic")
- `ANTHROPIC_API_KEY` - the API key for the [Anthropic API](https://www.anthropic.com/api). This is used only for Anthropic. 
- `ANTHROPIC_MODEL` - the model to use for the Anthropic API. This is used only for Anthropic.
- `OPENAI_API_KEY` - the API key for the [OpenAI API](https://openai.com/index/openai-api/). This is used only for OpenAI.
- `OPENAI_MODEL` - the model to use for the OpenAI API. This is used only for OpenAI.
- `OPENAI_EMBEDDING_MODEL` - the model to use for the OpenAI embedding API. We use embedding model for the memory module.

#### Agent settings

- `AGENT_PERSONALITY` - the personality of the agent. It's the general description of the agent, its beliefs, tone, etc.
- `AGENT_GOAL` - the goal of the agent. It's the general goal of the agent. We recommend making it short.
- `AGENT_REST_TIME` - the time in seconds the agent will rest between actions.

#### Integration settings

- `TELEGRAM_BOT_TOKEN` - the token for the Telegram bot. You can get it from the [BotFather](https://core.telegram.org/bots#botfather).
- `TELEGRAM_CHAT_ID` - the chat ID for the Telegram bot. Can be your own chat ID or the chat ID of the group/channel.
- `TWITTER_API_KEY` - the API key for the Twitter API.
- `TWITTER_API_SECRET_KEY` - the API secret key for the Twitter API.
- `TWITTER_ACCESS_TOKEN` - the access token for the Twitter API.
- `TWITTER_ACCESS_TOKEN_SECRET` - the access token secret for the Twitter API.
- `PERPLEXITY_API_KEY` - the API key for the [Perplexity API].
- `PERPLEXITY_ENDPOINT` - the endpoint for the Perplexity API.


## Contributing

Contributions are welcome! Please follow the [CONTRIBUTING](CONTRIBUTING.md) file for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
