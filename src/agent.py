import asyncio
from typing import Any, Optional

from loguru import logger

from src.core.config import settings
from src.core.state_enum import AgentState
from src.feedback.feedback_module import FeedbackModule
from src.memory.memory_module import get_memory_module
from src.planning.planning_module import PlanningModule
from src.workflows.analyze_signal import analyze_signal
from src.workflows.research_news import analyze_news_workflow


class Agent:
    """
    Central runtime for an autonomous AI agent. Integrates:
      1. Perception Module
      2. Memory Module
      3. Planning Module (Q-learning or other RL)
      4. Execution Module
      5. Feedback Module
      6. Autonomy Engine

    ### Adding a New State
      1. Open `core/state_enum.py`.
      2. Add the new state to the `AgentState` class.
        class AgentState(Enum):
            DEFAULT = "default"
            WAITING_FOR_NEWS = "waiting_for_news"
            NEW_STATE = "new_state"
    """

    def __init__(self):
        #: Initialize Memory Module
        self.memory_module = get_memory_module()

        #: Initialize Planning Module with persistent Q-table
        self.planning_module = PlanningModule(
            actions=[
                "idle",  # Do nothing (resting state)
                "check_news",  # Check if there are any news
                "post_to_telegram",  # Analyze news and post to Telegram
                "post_to_twitter",  # Analyze news and post to Twitter
            ],
            q_table_path=settings.PERSISTENT_Q_TABLE_PATH,  # Persistent Q-table file
        )

        #: Initialize Feedback Module
        self.feedback_module = FeedbackModule()

        #: Start in a default state
        self.state = AgentState.DEFAULT  # "default"

    # --------------------------------------------------------------
    # UTILITY FUNCTIONS FOR STATE & PLANNING & FEEDBACK
    # --------------------------------------------------------------

    def _update_state(self, last_action: str):
        """Updates the agent's state based on the last action."""
        if last_action == "check_news":
            self.state = AgentState.WAITING_FOR_NEWS
        elif last_action == "post_to_telegram":
            self.state = AgentState.JUST_POSTED_TO_TELEGRAM
        elif last_action == "post_to_twitter":
            self.state = AgentState.JUST_POSTED_TO_TWITTER
        elif last_action == "idle":
            self.state = AgentState.DEFAULT
        else:
            self.state = AgentState.DEFAULT

        logger.info(f"Agent state updated to: {self.state.name}")

    def _update_planning_policy(self, state: str, action: str, reward: float, next_state: str):
        """Update the Q-learning table in the PlanningModule."""
        self.planning_module.update_q_table(state, action, reward, next_state)

    def _collect_feedback(self, action: str, outcome: Optional[Any]) -> float:
        """Collect feedback for the action & outcome in the FeedbackModule."""
        return self.feedback_module.collect_feedback(action, outcome)

    # --------------------------------------------------------------
    # RL-based PLANNING & EXECUTION
    # --------------------------------------------------------------

    async def _perform_planned_action(self, action_name: str) -> Optional[str]:
        """Perform the planned action and return the outcome."""
        outcome = None

        # 1. Perform the action based on the action name (arg)
        if action_name == "idle":
            logger.info("Agent is idling.")
            outcome = "idle"

        elif action_name == "check_news":
            news = await analyze_signal()
            if news:
                logger.info("News perceived.")
                outcome = news
            else:
                logger.info("No news detected.")
                outcome = None

        elif action_name == "post_to_telegram":
            recent_news = "No recent news found"
            retrieved = await self.memory_module.search("news", top_k=1)
            if retrieved:
                recent_news = retrieved[0]["event"]
            outcome = await analyze_news_workflow(recent_news)
        elif action_name == "post_to_twitter":
            logger.warning(f"Twitter logic here: {action_name}")
            outcome = None
        else:
            logger.warning(f"Unknown action: {action_name}")
            outcome = None

        # 2. Store the outcome in memory
        event = f"Performed action '{action_name}'"
        await self.memory_module.store(
            event, action_name, str(outcome), metadata={"state": self.state}
        )

        # 3. Update the state
        self._update_state(action_name)
        return outcome

    # --------------------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------------------

    async def start_runtime_loop(self) -> None:
        logger.info("Starting the autonomous agent runtime loop...")

        while True:
            try:
                # 1. Choose an action
                #    You might treat the entire system as one "state", or define states.
                logger.debug(f"Current state: {self.state.name}")
                current_state = self.state.value
                action_name = self.planning_module.get_action(current_state)
                logger.debug(f"Action chosen: {action_name}")

                # 2. Perform that action
                outcome = await self._perform_planned_action(action_name)
                logger.debug(f"Outcome: {outcome}")

                # 3. Collect feedback
                reward = self._collect_feedback(action_name, outcome)
                logger.debug(f"Reward: {reward}")

                # 4. Update the planning policy
                next_state = self.state.value
                logger.debug(f"Next state: {next_state}")
                self._update_planning_policy(current_state, action_name, reward, next_state)

                # 4. Sleep or yield
                await asyncio.sleep(10)

            except KeyboardInterrupt:
                logger.info("Agent runtime loop interrupted by user.")
                break
            except Exception as e:
                logger.error(f"Error in runtime loop: {e}")
                break
