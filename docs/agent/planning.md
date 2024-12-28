# **Planning Module**

## Overview

The Planning Module is a core component of the Nevron autonomous AI agent. It uses [Q-learning](https://en.wikipedia.org/wiki/Q-learning), a model-free reinforcement learning algorithm, to make intelligent decisions based on the current system state. 

The module continuously adapts to new data via feedback loops while maintaining state-action value mappings for consistency.

At its core, the Planning Module:

- **Learns from experience**: It adapts its behavior based on feedback from the environment.
- **Balances exploration & exploitation**: It decides when to try new actions (exploration) and when to stick with actions it knows work well (exploitation).
- **Plans for the future**: It prioritizes long-term success while still considering immediate rewards.

-----

## How It Works

The Planning Module empowers the AI agent with sophisticated decision-making capabilities. Through continuous updates to the Q-table after each action, the agent refines and improves its decision-making process based on accumulated experience. 

When environmental conditions change, the agent demonstrates adaptability by swiftly learning new behavioral patterns through dynamic Q-table adjustments.

One of the key strengths is enabling autonomous operations - the agent can make informed decisions independently without requiring constant human oversight. Additionally, the module excels at managing complexity by helping the agent navigate and prioritize decisions effectively, even in environments with numerous possible states and actions.

In a nutshell, the **Q-table** is the memory of the Planning Module. It keeps track of:

- Each state the agent encounters.
- The actions available in that state.
- The expected reward for taking each action.

Over time, this table grows and becomes the agent’s primary reference for decision-making.

-----

## Core Components

### Configuration Parameters

The Planning Module's behavior is governed by several key configuration parameters that define its learning dynamics and decision-making capabilities.

All the parameters can be divided into two groups:

**Core Parameters**

- `actions`: Defines the action space available to the agent through a comprehensive list of permitted actions. By default, utilizes the `AgentAction` enumeration.
- `q_table_path`: Specifies the persistence location for the Q-learning table, enabling state preservation across sessions.

**Learning Parameters** 

- `planning_alpha`: (Learning Rate): Controls how quickly the agent learns from new experiences. A higher value (e.g. 0.9) means faster learning but potential instability, while a lower value (e.g. 0.1) means slower but more stable learning.

- `planning_gamma`: (Discount Factor): Determines how much the agent values future rewards vs immediate rewards. Values closer to 1 make the agent consider long-term consequences, while lower values like 0.5 make it focus on immediate rewards.

- `planning_epsilon`: (Exploration Rate): Controls the balance between exploring new actions vs exploiting known good actions. Higher values encourage trying new things in uncertain environments, while lower values stick to proven strategies in well-understood situations.

-----

If you have any questions or need further assistance, please refer to the [FAQ](faq.md) or initiate a discussion on our [GitHub Discussions](https://github.com/axioma-ai-labs/nevron/discussions).