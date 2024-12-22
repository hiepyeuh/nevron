from loguru import logger
import asyncio
from typing import Optional, Dict, Any
from src.tools import twitter, tg
import numpy as np
import httpx
import random

from src.planning_module import PlanningModule

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
        # 1. Perception, 2. Memory (omitted for brevity in this snippet)
        self.perception_module = None
        self.memory_module = None

        # 3. Initialize the planning module with some possible actions
        self.planning_module = PlanningModule(actions=[
            "check_news",         # Action that triggers _perceive to see if any new data arrived
            "post_to_telegram",   # Action to post something to telegram
            "post_to_twitter",    # Action to post something to twitter
        ])

        # 4. Execution Module: existing code to manage tools
        self.execution_tools = {
            "telegram": {
                "post_summary": tg.post_summary_to_telegram,
                "post_admin": tg.post_to_admin,
                "post_reviewers": tg.post_to_reviewers,
            },
            "twitter": {
                "post_thread": twitter.post_twitter_thread,
                "upload_media": twitter.upload_media_v1,
            }
        }

        # 5. Feedback Module (omitted for brevity)
        self.feedback_module = None

        # Simple agent state
        self.state = "default"

    async def _execute_action(self, action: str, data: Dict[str, Any]) -> Optional[Any]:
        logger.info(f"Executing action '{action}' with data: {data}")
        try:
            tool, method = action.split(".")
            if tool not in self.execution_tools or method not in self.execution_tools[tool]:
                logger.error(f"Invalid action '{action}'. Tool or method not found.")
                return None

            func = self.execution_tools[tool][method]
            result = await func(**data)
            logger.info(f"Action '{action}' executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error executing action '{action}': {e}")
            return None

    async def execute_telegram_action(self, method: str, **kwargs) -> Optional[Any]:
        return await self._execute_action(f"telegram.{method}", kwargs)

    async def execute_twitter_action(self, method: str, **kwargs) -> Optional[Any]:
        return await self._execute_action(f"twitter.{method}", kwargs)

    # --------------------------------------------------------------
    # RL-based PLANNING & EXECUTION
    # --------------------------------------------------------------

    def _collect_feedback(self, action: str, outcome) -> float:
        """
        Feedback Module:
        Here you define how to measure success/failure (reward).
        For example, if "post_to_telegram" fails, negative reward,
        if "check_news" found something, positive reward, etc.
        """
        logger.info(f"Collecting feedback for action '{action}'")
        if outcome is None:
            # e.g., big negative reward
            return -1.0
        else:
            # simplistic random reward or custom logic
            return float(np.random.choice([1.0, 0.0, -1.0]))

    def _update_planning_policy(self, state: str, action: str, reward: float, next_state: str) -> None:
        """
        Pass the parameters along to our Q-learning planning module.
        """
        self.planning_module.update_q_table(state, action, reward, next_state)

    async def _perform_planned_action(self, action_name: str):
        """
        Convert high-level action_name (like 'check_news') into actual code calls.
        """
        outcome = None

        if action_name == "check_news":
            # We can call _perceive to fetch from API
            news = await self._perceive()
            # We'll consider the outcome "good" if we got something
            outcome = news if news else None

        elif action_name == "post_to_telegram":
            # Example: post a summary
            outcome = await self.execute_telegram_action(
                "post_summary", summary_html="<b>Autonomous post</b>"
            )

        elif action_name == "post_to_twitter":
            # Example: post a short thread
            outcome = await self.execute_twitter_action(
                "post_thread", tweets={"tweet1": "Autonomous tweet!", "tweet2": "Thread part 2"}
            )
        
        # If you had more actions, handle them here.
        return outcome
    
    async def _fetch_signal(self) -> dict:
        """
        Fetch a signal from the API endpoint.

        Returns:
            dict: Parsed JSON response from the API. Expected format:
                  - {"status": "no_data"} when no actionable signal.
                  - {"status": "new_data", "news": "Some breaking news here."} when actionable signal.
        """
        api_url = "https://example.com/api/signal"  # Replace with the actual API URL

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"Signal fetched: {data}")
                    return data
                else:
                    logger.error(f"Failed to fetch signal. Status code: {response.status}")
                    return {"status": "error"}
        except Exception as e:
            logger.error(f"Error fetching signal from API: {e}")
            return {"status": "error"}

    async def _perceive(self) -> Optional[str]:
        """
        Perception Module (Slightly updated to allow direct calls)
        - This is the same function you had, just returning the news string if available.
        """
        signal = await self._fetch_signal()
        if signal.get("status") == "new_data" and "news" in signal:
            logger.info(f"Actionable signal received: {signal['news']}")
            return signal["news"]
        elif signal.get("status") == "no_data":
            logger.info("No actionable signal detected.")
            return None
        else:
            logger.warning("Received an unknown signal format or an error occurred.")
            return None

    # --------------------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------------------

    async def start_runtime_loop(self) -> None:
        logger.info("Starting the autonomous agent runtime loop...")
        
        while True:
            try:
                # 1. Choose an action
                #    You might treat the entire system as one "state", or define states.
                current_state = self.state
                action_name = self.planning_module.get_action(current_state)
                
                # 2. Perform that action
                outcome = await self._perform_planned_action(action_name)

                # 3. Collect feedback
                reward = self._collect_feedback(action_name, outcome)

                # 4. Update Q-table
                next_state = "default"  # or change if you track multiple states
                self._update_planning_policy(current_state, action_name, reward, next_state)

                # 5. Sleep or yield
                await asyncio.sleep(5)

            except KeyboardInterrupt:
                logger.info("Agent runtime loop interrupted by user.")
                break
            except Exception as e:
                logger.error(f"Error in runtime loop: {e}")
                break

    def _store_in_memory(self, key: str, value: str) -> None:
        """
        Memory Module:
        - Store the perceived data into Qdrant or other memory storage
        - Possibly do embeddings, vector indexing, or other transformations
        """
        # Example placeholder:
        # self.memory_module.store(key, value)
        pass

    def _get_environment_inputs(self) -> list:
        """
        Placeholder method to fetch new data from the environment.
        For example:
          - Poll Twitter for new mentions
          - Check an RSS feed for news
          - Observe internal triggers
        Return format: [("twitter", tweet_data), ("news", news_data), ...]
        """
        return []
