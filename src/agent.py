import asyncio
from typing import Any, Dict, List, Optional

import httpx
import numpy as np
from loguru import logger

from src.memory_module import MemoryModule
from src.planning_module import PlanningModule
from src.tools import tg, twitter


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
        # 1. Initialize Perception, Execution, and other modules
        self.perception_module = None
        self.memory_module = MemoryModule(
            collection_name="agent_memory",
            host="localhost",  # use the actual IP / domain
            port=6333,
            vector_size=768,
        )
        self.feedback_module = None

        # 2. Initialize Planning Module with persistent Q-table
        self.planning_module = PlanningModule(
            actions=[
                "check_news",  # Check if there are new signals
                "post_to_telegram",  # Post updates to Telegram
                "post_to_twitter",  # Post updates to Twitter
                "idle",  # Do nothing (resting state)
            ],
            q_table_path="persistent_q_table.json",  # Persistent Q-table file
        )

        # 3. Execution Tools
        self.execution_tools: Dict[str, Dict[str, Any]] = {
            "telegram": {
                "post_summary": tg.post_summary_to_telegram,
                "post_admin": tg.post_to_admin,
                "post_reviewers": tg.post_to_reviewers,
            },
            "twitter": {
                "post_thread": twitter.post_twitter_thread,
                "upload_media": twitter.upload_media_v1,
            },
        }

        # 4. Current State
        self.state = "default"  # Start in a default state

    async def _call_openai_api(self, prompt: str) -> str:
        """
        Placeholder for an OpenAI or other LLM call to analyze text.
        Replace this with a real API call in your production code.
        """
        logger.info(f"Calling OpenAI with prompt:\n{prompt}")
        # Simulate an AI-generated analysis
        return f"AI Analysis of the news: This news is about '{prompt}' (mock)."

    def _update_state(self, last_action: str):
        """
        Updates the agent's state based on the last action.

        Args:
            last_action (str): The action that was just performed.
        """
        if last_action == "check_news":
            self.state = "waiting_for_news"
        elif last_action == "post_to_telegram":
            self.state = "just_posted_to_telegram"
        elif last_action == "post_to_twitter":
            self.state = "just_posted_to_twitter"
        elif last_action == "idle":
            self.state = "default"  # Reset to default
        else:
            self.state = "default"  # Fallback
        logger.info(f"Agent state updated to: {self.state}")

    def _update_planning_policy(self, state: str, action: str, reward: float, next_state: str):
        """
        Update the Q-learning table in the PlanningModule.
        """
        self.planning_module.update_q_table(state, action, reward, next_state)

    async def _execute_action(self, action: str, data: Dict[str, Any]) -> Optional[Any]:
        logger.info(f"Executing action '{action}' with data: {data}")
        try:
            tool, method = action.split(".")
            if tool not in self.execution_tools:
                logger.error(f"Invalid tool '{tool}'")
                return None

            tool_methods = self.execution_tools[tool]
            if method not in tool_methods:
                logger.error(f"Invalid method '{method}' for tool '{tool}'")
                return None

            func = tool_methods[method]
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

    async def analyze_news_workflow(self, news: str) -> Optional[str]:
        """
        1) Analyze the news with an LLM (placeholder)
        2) Prepare a tweet
        3) Publish tweet on Twitter
        """
        try:
            # Step 1: Analyze the news
            analysis_prompt = f"Please analyze the following news:\n{news}"
            analysis = await self._call_openai_api(analysis_prompt)

            # Step 2: Prepare tweet (simple example)
            # You might incorporate the analysis into the tweet
            tweet_text = f"Breaking News:\n{analysis}\n#StayInformed"

            # Step 3: Publish tweet on Twitter
            logger.info(f"Preparing to post tweet:\n{tweet_text}")
            result = await self.execute_twitter_action("post_thread", tweets={"tweet1": tweet_text})
            logger.info("Tweet posted successfully!")
            return result
        except Exception as e:
            logger.error(f"Error in analyze_news_workflow: {e}")
            return None

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

    async def _perform_planned_action(self, action_name: str):
        """
        Executes the planned action and updates the state.

        Args:
            action_name (str): The name of the planned action.
        """
        outcome = None
        if action_name == "check_news":
            # Fetch news and transition to the appropriate state
            news = await self._perceive()
            outcome = news if news else None

        elif action_name == "post_to_telegram":
            # Post a summary to Telegram
            outcome = await self.execute_telegram_action(
                "post_summary", summary_html="<b>Autonomous post</b>"
            )

        elif action_name == "post_to_twitter":
            # Post a thread to Twitter
            outcome = await self.execute_twitter_action(
                "post_thread", tweets={"tweet1": "Autonomous tweet!", "tweet2": "Thread part 2"}
            )

        elif action_name == "idle":
            # Do nothing and just wait
            logger.info("Agent is idling.")
            outcome = "idle"

        # --- NEW WORKFLOW ---
        elif action_name == "analyze_news":
            # For demonstration, you might fetch the last perceived news or do a new perception:
            # If you want to re-use the last news from memory, you could do so:
            recent_news = "No recent news found"
            # Example: try retrieving the last stored news from memory
            # (this is optional logic if you want to pull from memory)
            retrieved = self.memory_module.search("news", top_k=1)
            if retrieved:
                recent_news = retrieved[0]["content"]

            outcome = await self.analyze_news_workflow(recent_news)

        else:
            logger.warning(f"Unknown action: {action_name}")
            outcome = None

        # Update the state after performing the action
        self._update_state(action_name)

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
                    logger.error(f"Failed to fetch signal. Status code: {response.status_code}")
                    return {"status": "error"}
        except Exception as e:
            logger.error(f"Error fetching signal from API: {e}")
            return {"status": "error"}

    async def _perceive(self) -> Optional[str]:
        signal = await self._fetch_signal()
        if signal.get("status") == "new_data" and "news" in signal:
            news = signal["news"]
            logger.info(f"Actionable signal received: {news}")

            # Store the news in memory
            self.memory_module.store(news, metadata={"type": "news"})

            return news
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
                next_state = self.state  # After performing, we’re in the updated state
                self._update_planning_policy(current_state, action_name, reward, next_state)

                # 4. Sleep or yield
                await asyncio.sleep(5)

            except KeyboardInterrupt:
                logger.info("Agent runtime loop interrupted by user.")
                break
            except Exception as e:
                logger.error(f"Error in runtime loop: {e}")
                break

    def recall_recent_news(self, query: str = "latest news") -> List[str]:
        search_results = self.memory_module.search(query, top_k=3)
        contents = [res["content"] for res in search_results]
        return contents
