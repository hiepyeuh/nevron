from typing import Optional

from loguru import logger

from src.llm.llm import LLM
from src.memory.memory_module import MemoryModule, get_memory_module
from src.tools.get_signal import fetch_signal
from src.tools.twitter import post_twitter_thread


async def analyze_signal(memory: MemoryModule = get_memory_module()) -> Optional[str]:
    """
    Fetch a signal, analyze it with an LLM, and post the result on Twitter.

    Returns:
        Optional[str]: Twitter post result or None if an error occurred.
    """
    try:
        logger.info("Fetching signal...")
        signal = await fetch_signal()

        if signal.get("status") == "new_data" and "news" in signal:
            news = signal["news"]
            logger.info(f"Actionable signal received: {news}")

            logger.info("Analyzing signal...")
            # Retrieve recent memory for context
            recent_memories = await memory.search("recent events", top_k=3)
            context = "\n".join([f"- {mem['event']}: {mem['outcome']}" for mem in recent_memories])

            # Prepare LLM prompt
            llm = LLM()
            user_prompt = (
                f"Context:\n{context}\n\nNews:\n{news}\n\n"
                "Analyze the news and provide insights. "
                "Finally make a concise tweet about the news with a maximum of 280 characters."
            )
            messages = [{"role": "user", "content": user_prompt}]
            analysis = await llm.generate_response(messages)

            # Prepare tweet
            tweet_text = f"Breaking News:\n{analysis}\n#CryptoNews"

            # Publish tweet
            logger.info(f"Publishing tweet:\n{tweet_text}")
            result = await post_twitter_thread(tweets={"tweet1": tweet_text})
            logger.info("Tweet posted successfully!")
            return ";".join(str(res) for res in result)

        elif signal.get("status") == "no_data":
            logger.info("No actionable signal detected.")
            return None
        else:
            logger.warning("Received an unknown signal format or an error occurred.")
            return None

    except Exception as e:
        logger.error(f"Error in analyze_and_post_signal workflow: {e}")
        return None
