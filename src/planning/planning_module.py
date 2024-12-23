import json
import random
from pathlib import Path

from loguru import logger

from src.core.config import settings


class PlanningModule:
    """A simple Q-learning planning module for high-level autonomous decisions."""

    #: TODO: Implement alpha, gamma, epsilon as settings
    def __init__(
        self,
        actions=None,
        alpha=0.1,
        gamma=0.95,
        epsilon=0.1,
        q_table_path=settings.PERSISTENT_Q_TABLE_PATH,
    ):
        """
        Args:
            actions (List[str]): A list of strings representing possible actions
            (e.g., ['idle', 'analyze_signal', 'research_news']).
            alpha (float): Learning rate for Q-learning.
            gamma (float): Discount factor for future rewards.
            epsilon (float): Probability for exploration in epsilon-greedy policy.
            q_table_path (str): Path to the file where the Q-table is saved.
        """
        #: TODO: Implement actions as settings or definition! Update it also in the agent.py
        if actions is None:
            actions = [
                "idle",
                "analyze_signal",
                "research_news",
            ]

        self.actions = actions
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
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
                    logger.info(f"Loaded Q-table from {self.q_table_path}")
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
                logger.info(f"Q-table saved to {self.q_table_path}")
        except Exception as e:
            logger.error(f"Failed to save Q-table: {e}")

    def get_action(self, state: str) -> str:
        """
        Select an action using epsilon-greedy policy.

        Args:
            state (str): The agent's current state key.

        Returns:
            str: The chosen action name.
        """
        # Ensure there's a Q-value array for this state
        if state not in self.q_table:
            self.q_table[state] = [0.0] * len(self.actions)

        # Epsilon-greedy selection
        if random.random() < self.epsilon:
            # Explore: pick a random action
            return random.choice(self.actions)
        else:
            # Exploit: pick the action with the highest Q-value
            state_q_values = self.q_table[state]
            max_q = max(state_q_values)
            max_indices = [i for i, q_val in enumerate(state_q_values) if q_val == max_q]
            return self.actions[random.choice(max_indices)]  # break ties at random

    def update_q_table(self, state, action, reward, next_state):
        """
        Update the Q-table using the Q-learning formula.

        Args:
            state (str): Current state.
            action (str): Action taken in this state.
            reward (float): Reward received after performing the action.
            next_state (str): Next state after the action.
        """
        # Ensure Q-value arrays exist
        if state not in self.q_table:
            self.q_table[state] = [0.0] * len(self.actions)
        if next_state not in self.q_table:
            self.q_table[next_state] = [0.0] * len(self.actions)

        action_idx = self.actions.index(action)
        current_q = self.q_table[state][action_idx]

        # Q-learning update
        max_next_q = max(self.q_table[next_state])
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)

        # Update the table
        self.q_table[state][action_idx] = new_q

        # Save the updated Q-table
        self._save_q_table()
