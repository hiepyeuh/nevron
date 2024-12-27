from loguru import logger

from src.core.config import settings
from src.tools.search_with_perplexity import search_with_perplexity


async def fetch_signal() -> dict:
    """
    Fetch a crypto signal from the coingecko API endpoint.

    Returns:
        dict: Parsed JSON response containing actionable crypto news or updates.
    """
    api_url = "https://api.coingecko.com/api/v3/news"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            if response.status_code == 200:
                data = response.json()
                logger.debug(f"Signal fetched: {data}")
                return {"status": "new_data", "news": data[0]["title"]}
            else:
                logger.error(f"Failed to fetch signal. Status code: {response.status_code}")
                return {"status": "no_data"}
    except Exception as e:
        logger.error(f"Error fetching signal from API: {e}")
        return {"status": "error"}
    if data:
        logger.info(f"Signal fetched: {data}")
        return {"status": "new_data", "news": data}
    else:
        logger.info(f"No data available: {data}")
        return {"status": "no_data"}
