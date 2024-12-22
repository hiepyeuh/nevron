from loguru import logger
import asyncio
from typing import Optional, Dict, Any
from src.tools import twitter, tg
import numpy as np
import httpx


class Agent:
    """
    Central runtime for an autonomous AI agent. Integrates:
      1. Perception Module
      2. Memory Module
      3. Planning Module (Q-learning or other RL)
      4. Execution Module
      5. Feedback Module
      6. Autonomy Engine

    The methods below are placeholders for you to fill in with actual implementations.
    """

    def __init__(self):
        """
        Initialize the agent with all required modules and execution tools
        """
        self.perception_module = None
        self.memory_module = None
        self.planning_module = None 
        
        # Initialize execution tools
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
        
        self.feedback_module = None

    async def _execute_action(self, action: str, data: Dict[str, Any]) -> Optional[Any]:
        """
        Execute actions using the configured tools.
        
        Args:
            action (str): Action identifier in format "tool.method" (e.g. "telegram.post_summary")
            data (Dict[str, Any]): Parameters for the action
            
        Returns:
            Optional[Any]: Result of the action execution
        """
        logger.info(f"Executing action '{action}' with data: {data}")
        
        try:
            # Parse tool and method from action string
            tool, method = action.split(".")
            
            if tool not in self.execution_tools or method not in self.execution_tools[tool]:
                logger.error(f"Invalid action '{action}'. Tool or method not found.")
                return None
                
            # Get the function to execute
            func = self.execution_tools[tool][method]
            
            # Execute the function
            result = await func(**data)
            logger.info(f"Action '{action}' executed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error executing action '{action}': {e}")
            return None

    async def execute_telegram_action(self, method: str, **kwargs) -> Optional[Any]:
        """
        Execute Telegram-specific actions
        
        Args:
            method (str): Telegram method to execute
            **kwargs: Arguments for the method
            
        Returns:
            Optional[Any]: Result of the telegram action
        """
        return await self._execute_action(f"telegram.{method}", kwargs)

    async def execute_twitter_action(self, method: str, **kwargs) -> Optional[Any]:
        """
        Execute Twitter-specific actions
        
        Args:
            method (str): Twitter method to execute
            **kwargs: Arguments for the method
            
        Returns:
            Optional[Any]: Result of the twitter action
        """
        return await self._execute_action(f"twitter.{method}", kwargs)

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
        Perception Module:
        - Calls an API to fetch a signal.
        - Processes the signal to determine if there's actionable data.

        Returns:
            Optional[str]: The actionable news string if available, or None otherwise.
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

    # Updated runtime loop to include Perception Module
    async def start_runtime_loop(self) -> None:
        """Start the agent's autonomous runtime loop."""
        logger.info("Starting the autonomous agent runtime loop...")

        while True:
            try:
                # Step 1: Perception - Fetch and process signals
                actionable_data = await self._perceive()

                if actionable_data:
                    # Step 2: Trigger a reaction (e.g., post to Telegram or Twitter)
                    # Example: Post to Telegram with the news data
                    await self.execute_telegram_action(
                        "post_summary",
                        summary_html=f"<b>Breaking News:</b> {actionable_data}"
                    )

                # Sleep or yield to prevent a tight loop
                await asyncio.sleep(5)

            except KeyboardInterrupt:
                logger.info("Agent runtime loop interrupted by user.")
                break
            except Exception as e:
                logger.error(f"Error in runtime loop: {e}")
                break

    def _autonomy_engine(self, inputs) -> None:
        """
        The main orchestration method that runs:
          1. Perception  
          2. Memory update/retrieval  
          3. Planning (which action to take)  
          4. Execution of that action  
          5. Feedback collection  
          6. Update Q-table or RL policy  
        """
        # For each piece of input, run the chain of modules
        for source, data in inputs:
            # 1. Perception
            perceived_data = self._perceive(source, data)

            # 2. Memory
            self._store_in_memory(source, perceived_data)

            # 3. Planning
            action = self._plan_action(perceived_data)

            # 4. Execution
            outcome = self._execute_action(action, perceived_data)

            # 5. Feedback
            reward = self._collect_feedback(action, outcome)

            # 6. Update Q-learning or RL policy
            self._update_planning_policy(perceived_data, action, reward)

    def _store_in_memory(self, key: str, value: str) -> None:
        """
        Memory Module:
        - Store the perceived data into Qdrant or other memory storage
        - Possibly do embeddings, vector indexing, or other transformations
        """
        # Example placeholder:
        # self.memory_module.store(key, value)
        pass

    def _plan_action(self, state: str) -> int:
        """
        Planning Module (Q-learning or other RL):
        - Based on the perceived state, choose which action to take next
        - Return the action ID or descriptor
        """
        # Example placeholder:
        # action = self.planning_module.choose_action(state)
        return np.random.randint(0, 3)  # e.g., random action

    def _collect_feedback(self, action: int, outcome) -> float:
        """
        Feedback Module:
        - Gather feedback (user rating, success/failure, etc.)
        - Return a reward signal for reinforcement learning
        """
        # Example placeholder:
        # feedback = self.feedback_module.get_feedback(action, outcome)
        # return feedback
        logger.info(f"Collecting feedback for action {action}")
        reward = np.random.choice([1.0, -1.0])  # random positive/negative
        return reward

    def _update_planning_policy(self, state: str, action: int, reward: float) -> None:
        """
        Update the Q-table or policy with the new reward signal
        """
        # Example placeholder:
        # self.planning_module.update_q_table(state, action, reward)
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