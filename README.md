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

This is a simple autonomous agent that uses Q-learning to make decisions, integrates with 
Telegram and Twitter, and uses Qdrant for vector storage as a memory module.

Description of the agent in bullet points:

- This autonomous agent is designed to perform the tasks on his own. 
- The core of the agent is implemented by planning, feedback and memory modules. 
- The real intelligence is powered by LLMs. Currently we support OpenAI and Anthropic.
- The actions of the agent are defined in workflows, which encapsulate logic of performing the task.
- Different 3rd party services are integrated with the agent via tools, which are used in the workflows. Example of the tools:
  - Telegram
  - Twitter
  - Some API for getting news (not implemented yet)
  - Perplexity for research (not implemented yet)

Some more details about some modules:

### Planning module

The planning module is responsible for making decisions and planning the next action. It uses the Q-learning algorithm to make decisions. The details can be found in code at the [planning_module.py](src/planning/planning_module.py) file.

### Feedback module

The feedback module is responsible for providing feedback to the agent and updating the Q-learning model (in Planning module). It uses the feedback from the previous action, such as the result of the action and type of the action, to evaluate the result of the action and give this result to the Planning module (to update the Q-learning model). The details can be found in code at the [feedback_module.py](src/feedback/feedback_module.py) file.

### Memory module

The memory module is responsible for storing the memories of the agent: what actions were performed, what was the result of the action, etc. It uses Qdrant for storing the memories. The details can be found in code at the [memory_module.py](src/memory/memory_module.py) file.  

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

### Docker

You need to have Docker installed for running the Qdrant container. Install this software first (follow the official documentation).

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

You can use the provided `.env.dev` file to setup the environment variables. 

```
cp .env.dev .env
```

### Run the Agent

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

Run the agent:

```bash
make run
```

Alternatively, you can run the agent manually:

```bash
pipenv run python -m src.main
```

## Contributing

Contributions are welcome! Please follow the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
