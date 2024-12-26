import json
import random
from pathlib import Path

from loguru import logger

from src.core.config import settings
from src.core.defs import AgentAction, AgentState


class PlanningModule:
    """A simple Q-learning planning module for high-level autonomous decisions."""

    def __init__(
        self,
        actions=None,
        q_table_path=settings.PERSISTENT_Q_TABLE_PATH,
        planning_alpha=settings.PLANNING_ALPHA,
        planning_gamma=settings.PLANNING_GAMMA,
        planning_epsilon=settings.PLANNING_EPSILON,
    ):
        """
        Initialize the planning module.

        Tuning Tips:
        - PLANNING_ALPHA:
        - Increase for faster adaptation but risk instability.
        - Decrease for more stable but slower learning.
        - PLANNING_GAMMA:
        - Set closer to 1 for long-term planning.
        - Set lower (e.g., 0.5) for short-term rewards.
        - PLANNING_EPSILON:
        - Increase to encourage exploration in unpredictable environments.
        - Decrease for environments where optimal actions are well-known.

        Args:
            actions (List[str]): A list of strings representing possible actions
                                (e.g., ['idle', 'analyze_signal', 'research_news']). Note, that the
                                actions are from the AgentAction enum.
            q_table_path (str): Path to the file where the Q-table is saved.
            planning_alpha (float): The learning rate for the Q-learning algorithm. Controls how
                                  quickly the agent adapts to new information. Default: `0.1`.
            planning_gamma (float): The discount factor for future rewards. Determines how much
                                    importance is given to long-term rewards. Default: `0.95`.
            planning_epsilon (float): The exploration rate for the epsilon-greedy strategy. Higher
                                    values encourage exploration, while lower values favor
                                    exploitation. Default: `0.1`.
        """
        if actions is None:
            actions = list(AgentAction)

        self.actions = actions

        # Fetch Q-learning parameters from settings
        self.alpha = planning_alpha  # Learning rate for Q-learning (float)
        self.gamma = planning_gamma  # Discount factor for future rewards (float)
        self.epsilon = (
            planning_epsilon  # Probability for exploration in epsilon-greedy policy (float)
        )
        self.q_table_path = Path(q_table_path)

        # Load Q-table from file if it exists, otherwise initialize an empty table
        self.q_table = self._load_q_table()

    def _load_q_table(self) -> dict:
        """
        Load the Q-table from a JSON file if it exists.

        Returns:
            dict: The loaded Q-table or an empty dictionary if the file does not exist.
        """
        if self.q_table_path.exists():
            try:
                with open(self.q_table_path, "r") as file:
                    q_table = json.load(file)
                    logger.debug(f"Loaded Q-table from {self.q_table_path}")
                    return q_table
            except Exception as e:
                logger.error(f"Failed to load Q-table: {e}")
        return {}

    def _save_q_table(self) -> None:
        """
        Save the Q-table to a JSON file.
        """
        try:
            with open(self.q_table_path, "w") as file:
                json.dump(self.q_table, file, indent=4)
                logger.debug(f"Q-table saved to {self.q_table_path}")
        except Exception as e:
            logger.error(f"Failed to save Q-table: {e}")

    def get_action(self, state: AgentState) -> AgentAction:
        """
        Select an action using epsilon-greedy policy.

        Args:
            state (AgentState): The agent's current state.

        Returns:
            AgentAction: The chosen action.
        """
        # Ensure there's a Q-value array for this state
        state_key = state.value
        if state_key not in self.q_table:
            self.q_table[state_key] = [0.0] * len(self.actions)
            logger.debug(f"State {state_key} not found in Q-table. Initialized with zeros.")

        # Epsilon-greedy selection
        if random.random() < self.epsilon:
            # Explore: pick a random action
            return random.choice(self.actions)
        else:
            # Exploit: pick the action with the highest Q-value
            state_q_values = self.q_table[state_key]
            max_q = max(state_q_values)
            max_indices = [i for i, q_val in enumerate(state_q_values) if q_val == max_q]
            return self.actions[random.choice(max_indices)]  # break ties at random

    def update_q_table(
        self, state: AgentState, action: AgentAction, reward: float, next_state: AgentState
    ):
        """
        Update the Q-table using the Q-learning formula.

        Args:
            state (AgentState): Current state.
            action (AgentAction): Action taken in this state.
            reward (float): Reward received after performing the action.
            next_state (AgentState): Next state after the action.
        """
        # Ensure Q-value arrays exist
        state_key = state.value
        next_state_key = next_state.value
        if state_key not in self.q_table:
            self.q_table[state_key] = [0.0] * len(self.actions)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = [0.0] * len(self.actions)

        action_idx = self.actions.index(action)
        current_q = self.q_table[state_key][action_idx]

        # Q-learning update
        max_next_q = max(self.q_table[next_state_key])
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)

        # Update the table
        self.q_table[state_key][action_idx] = new_q

        # Save the updated Q-table
        self._save_q_table()
