import httpx
from loguru import logger


async def fetch_signal() -> dict:
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
                logger.debug(f"Signal fetched: {data}")
                return data
            else:
                logger.error(f"Failed to fetch signal. Status code: {response.status_code}")
                return {"status": "error"}
    except Exception as e:
        logger.error(f"Error fetching signal from API: {e}")
        return {"status": "error"}
