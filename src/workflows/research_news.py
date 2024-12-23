from typing import Optional

from loguru import logger

from src.llm.oai_client import call_openai_api
from src.memory.memory_module import MemoryModule, get_memory_module
from src.tools.twitter import post_twitter_thread


async def analyze_news_workflow(
    news: str, memory: MemoryModule = get_memory_module()
) -> Optional[str]:
    """
    1) Analyze the news with an LLM
    2) Prepare a tweet
    3) Publish tweet on Twitter
    """
    try:
        # Retrieve recent memory for context
        recent_memories = await memory.search("recent events", top_k=3)
        context = "\n".join([f"- {mem['event']}: {mem['outcome']}" for mem in recent_memories])

        # Prepare LLM prompt
        prompt = f"Context:\n{context}\n\nNews:\n{news}\n\nAnalyze the news and provide insights."
        analysis = await call_openai_api(prompt)

        # Prepare tweet
        tweet_text = f"Breaking News:\n{analysis}\n#StayInformed"

        # Publish tweet
        logger.info(f"Publishing tweet:\n{tweet_text}")
        result = await post_twitter_thread(tweets={"tweet1": tweet_text})
        logger.info("Tweet posted successfully!")
        return ";".join(str(res) for res in result)
    except Exception as e:
        logger.error(f"Error in analyze_news_workflow: {e}")
        return None
