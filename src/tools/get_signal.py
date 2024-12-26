import httpx
from loguru import logger


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
