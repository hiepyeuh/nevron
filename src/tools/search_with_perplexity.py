import httpx
from loguru import logger

from src.core.config import settings
from src.core.exceptions import APIError


async def search_with_perplexity(query: str) -> str:
    """
    Perform a Perplexity search for the latest cryptocurrency news.
    Args:
        query (str): The search query (e.g., "Latest cryptocurrency news").

    Returns:
        str: Search results or an error message.
    """
    try:
        if not settings.PERPLEXITY_API_KEY:
            raise APIError("Perplexity API key is not set")
        if not settings.PERPLEXITY_ENDPOINT:
            raise APIError("Perplexity endpoint is not set")

        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a capable and efficient search assistant. "
                        "Your job is to find relevant and concise information about cryptocurrencies "
                        "based on the query provided."
                        "Validate the results for relevance and clarity. "
                    ),
                },
                {
                    "role": "user",
                    "content": f"Search for the latest cryptocurrency news: {query}",
                },
            ],
            "temperature": 0.3,
            "top_p": 0.8,
            "search_domain_filter": ["perplexity.ai"],  # Use default domain filter
            "return_images": False,
            "return_related_questions": False,
            "stream": False,
        }

        headers = {
            "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(
            verify=False
        ) as client:  # verify=True to enable SSL verification
            response = await client.post(
                settings.PERPLEXITY_ENDPOINT, json=payload, headers=headers
            )
            response.raise_for_status()
            data = response.json()

        logger.debug(f"Perplexity Search | Successfully retrieved results: {data}")
        summary = (
            data.get("choices", [{}])[0].get("message", {}).get("content", "No summary available.")
        )  # data.get("summary", "No summary available.")

        # Get the total tokens used from the response
        total_tokens = data.get("usage", {}).get("total_tokens", 0)

        # Estimate the cost
        estimated_cost = estimate_perplexity_cost_per_request(total_tokens)
        logger.debug(f"Estimated cost for the request: ${estimated_cost:.6f}")
        return f"Perplexity Search Results:\n{summary}"
    except httpx.TimeoutException as e:
        logger.error(f"Timeout during Perplexity search: {str(e)}")
        return "Perplexity search data is currently unavailable due to a timeout error."
    except Exception as e:
        logger.error(f"Error during Perplexity search: {str(e)}")
        return "Perplexity search data is currently unavailable."


def estimate_perplexity_cost_per_request(total_tokens: int) -> float:
    """
    Estimate the cost per request for the Perplexity search.

    Args:
        total_tokens (int): Total number of tokens used in the prompt + completion.

    Returns:
        float: Estimated cost of the request.
    """
    # Define the cost per token
    TOKEN_COST_PER_MILLION = (
        0.2  # $0.2 per 1M tokens (ref: https://docs.perplexity.ai/guides/pricing)
    )
    TOKEN_COST = TOKEN_COST_PER_MILLION / 1_000_000  # Cost per token

    # Calculate the estimated cost
    estimated_cost = total_tokens * TOKEN_COST
    return estimated_cost
