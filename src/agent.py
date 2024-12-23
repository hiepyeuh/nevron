import asyncio
from typing import Any, Optional

from loguru import logger

from src.core.config import settings
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
    """

    def __init__(self):
        #: Initialize Memory Module
        self.memory_module = get_memory_module()

        #: Initialize Planning Module with persistent Q-table
        #: TODO: Implement actions as settings or definition! Update this in the planning_module.py as well
        self.planning_module = PlanningModule(
            actions=[
                "check_signal",  # Check if there are new signals
                "research_news",  # Analyze news and post to Twitter
                "idle",  # Do nothing (resting state)
            ],
            q_table_path=settings.PERSISTENT_Q_TABLE_PATH,  # Persistent Q-table file
        )

        #: Initialize Feedback Module
        self.feedback_module = FeedbackModule()

        #: Start in a default state
        self.state = "default"

    # --------------------------------------------------------------
    # UTILITY FUNCTIONS FOR STATE & PLANNING & FEEDBACK
    # --------------------------------------------------------------

    def _update_state(self, last_action: str):
        """Updates the agent's state based on the last action."""
        if last_action == "check_signal":
            self.state = "waiting_for_signal"
        elif last_action == "research_news":
            self.state = "just_analyzed_news"
        elif last_action == "idle":
            self.state = "default"  # Reset to default
        else:
            self.state = "default"  # Fallback
        logger.info(f"Agent state updated to: {self.state}")

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

        elif action_name == "check_signal":
            news = await analyze_signal()
            if news:
                logger.info("News perceived.")
                outcome = news
            else:
                logger.info("No news detected.")
                outcome = None

        elif action_name == "research_news":
            recent_news = "No recent news found"
            retrieved = await self.memory_module.search("news", top_k=1)
            if retrieved:
                recent_news = retrieved[0]["event"]
            outcome = await analyze_news_workflow(recent_news)

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
                logger.debug(f"Current state: {self.state}")
                current_state = self.state
                action_name = self.planning_module.get_action(current_state)
                logger.debug(f"Action chosen: {action_name}")

                # 2. Perform that action
                outcome = await self._perform_planned_action(action_name)
                logger.debug(f"Outcome: {outcome}")

                # 3. Collect feedback
                reward = self._collect_feedback(action_name, outcome)
                logger.debug(f"Reward: {reward}")

                # 4. Update the planning policy
                next_state = self.state
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
