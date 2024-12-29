# **Planning Module**

## Overview

The Planning Module is a critical component of the Nevron autonomous AI agent. It leverages [Q-learning](https://en.wikipedia.org/wiki/Q-learning), a model-free reinforcement learning algorithm, to make intelligent decisions based on the current system state.

Key capabilities include:

- **Learning from experience**: Adapts behavior based on feedback from the environment.
- **Balancing exploration and exploitation**: Chooses between trying new actions (exploration) and relying on known effective actions (exploitation).
- **Planning for the future**: Prioritizes long-term success while considering immediate rewards.

The module continuously evolves by adapting to new data through feedback loops, while maintaining consistent state-action value mappings.

The Planning Module is implemented in `src/planning/planning_module.py`.
---

## How It Works

The Planning Module empowers the AI agent with sophisticated decision-making capabilities. It utilizes a **Q-table** to record and update state-action value mappings, which guide the agent's decisions. This process enables the agent to refine its behavior through accumulated experience.

Key functionalities include:

1. **Dynamic Adaptability**: When environmental conditions change, the module quickly updates the Q-table to learn new behavioral patterns.

2. **Autonomous Operations**: The agent independently makes informed decisions, reducing the need for constant human intervention.

3. **Managing Complexity**: Effectively navigates and prioritizes decisions in environments with numerous states and actions.

The **Q-table** acts as the module's memory, tracking:

- States encountered by the agent.
- Available actions for each state.
- Expected rewards for each action.

Over time, this table becomes the primary reference for decision-making, ensuring the agent operates effectively in both familiar and new situations.

---

## Core Components

The Planning Module's behavior is controlled by several configuration parameters that define its learning dynamics and decision-making capabilities. These parameters are categorized into:

#### Core Parameters

- **`actions`**: Defines the action space available to the agent, typically using the `AgentAction` enumeration to ensure a comprehensive list of permitted actions.
- **`q_table_path`**: Specifies the file path for saving and loading the Q-table, enabling state preservation across sessions.

#### Learning Parameters

- **`planning_alpha` (Learning Rate)**:
    - Controls how quickly the agent learns from new experiences.
    - Higher values (e.g., 0.9): Faster learning but potentially less stability.
    - Lower values (e.g., 0.1): Slower but more stable learning.

- **`planning_gamma` (Discount Factor)**:
    - Balances the importance of future rewards versus immediate ones.
    - Values closer to 1: Focus on long-term consequences.
    - Lower values (e.g., 0.5): Emphasis on immediate rewards.

- **`planning_epsilon` (Exploration Rate)**:
    - Determines the balance between exploration (trying new actions) and exploitation (sticking to known strategies).
    - Higher values: Encourages trying new actions in uncertain environments.
    - Lower values: Relies on proven strategies in well-understood scenarios.

---

If you have any questions or need further assistance, please refer to the [GitHub Discussions](https://github.com/axioma-ai-labs/nevron/discussions).