import numpy as np
import random

class PlanningModule:
    """
    A simple Q-learning planning module for high-level autonomous decisions.
    """

    def __init__(self, actions=None, alpha=0.1, gamma=0.95, epsilon=0.1):
        """
        Args:
            actions (List[str]): A list of strings representing possible actions (e.g., ['check_news', 'post_tweet', 'research']).
            alpha (float): Learning rate for Q-learning.
            gamma (float): Discount factor for future rewards.
            epsilon (float): Probability for exploration in epsilon-greedy policy.
        """
        if actions is None:
            actions = ["check_news", "post_to_telegram", "post_to_twitter"]
        
        self.actions = actions  
        self.alpha = alpha     # Learning rate
        self.gamma = gamma     # Discount factor
        self.epsilon = epsilon # Exploration rate

        # Q-table stored as { state: [Q-values for each action] }
        # In a simple scenario, we might treat the entire agent as having just one "state",
        # or you can expand with multiple states if you track different situations.
        self.q_table = {}
    
    def get_action(self, state):
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