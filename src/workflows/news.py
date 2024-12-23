"""Workflow system for automated tasks execution."""

from abc import ABC, abstractmethod
from typing import Any


class BaseWorkflow(ABC):
    """Base class for all workflows."""

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the workflow."""
        pass


class NewsAnalysisWorkflow(BaseWorkflow):
    """Workflow for analyzing news, summarizing them with OpenAI, and publishing to Twitter."""

    def __init__(self, oai_client, twitter_client):
        """Initialize the workflow with required clients."""
        self.oai_client = oai_client
        self.twitter_client = twitter_client

    def execute(self, news_text: str) -> dict:
        """
        Execute the news analysis workflow.

        Args:
            news_text (str): The news text to analyze

        Returns:
            dict: Result containing summary and tweet status
        """
        # Step 1: Analyze and summarize the news using OpenAI
        summary = self._summarize_news(news_text)

        # Step 2: Publish to Twitter
        tweet_status = self._publish_to_twitter(summary)

        return {"summary": summary, "tweet_status": tweet_status}

    def _summarize_news(self, news_text: str) -> str:
        """Summarize the news using OpenAI."""
        # Here we'll use the OpenAI client to generate a summary
        # The exact prompt and parameters can be customized based on needs
        response = self.oai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional news summarizer. Create a concise, engaging summary suitable for Twitter (max 280 characters).",
                },
                {"role": "user", "content": news_text},
            ],
            max_tokens=100,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def _publish_to_twitter(self, summary: str) -> dict:
        """Publish the summary to Twitter."""
        return self.twitter_client.post_tweet(summary)
