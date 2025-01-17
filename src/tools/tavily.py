from typing import Dict, List, Optional

import httpx
from tavily import AsyncTavilyClient

from src.core.config import settings


async def initialize_tavily_client(
    api_key: str = settings.TAVILY_API_KEY,
) -> AsyncTavilyClient:
    """
    Authenticate and return an Async Tavily client instance with SSL verification disabled.

    Args:
        api_key (str): Tavily API key. Defaults to value from settings.

    Returns:
        AsyncTavilyClient: Authenticated async Tavily client.
    """
    # Create the client with a custom client_creator that disables SSL verification
    client = AsyncTavilyClient(api_key=api_key)
    client._client_creator = lambda: httpx.AsyncClient(
        headers={"Content-Type": "application/json"},
        base_url="https://api.tavily.com",
        timeout=180,
        verify=False,  # Disable SSL verification for development
    )

    return client


async def execute_search(
    client: AsyncTavilyClient, query: str, filters: Optional[Dict] = None
) -> Dict:
    """
    Execute a search query using Tavily asynchronously.

    Args:
        client (AsyncTavilyClient): Authenticated async Tavily client.
        query (str): Search query string.
        filters (dict, optional): Additional filters for refining the search.
            Supported filters include:
            - search_depth: "basic" or "advanced"
            - include_domains: list of domains to include
            - exclude_domains: list of domains to exclude
            - max_results: maximum number of results (default: 5)

    Returns:
        dict: Search results containing 'results' list with search findings
    """
    search_params = {}
    if filters:
        search_params.update(filters)

    return await client.search(query=query, **search_params)


def parse_search_results(results: Dict) -> List[Dict]:
    """
    Parse and structure Tavily search results.

    Args:
        results (dict): Raw search results from Tavily.

    Returns:
        list: List of processed results, each containing:
            - title: str
            - url: str
            - content: str
            - score: float
            - published_date: str (if available)
    """
    parsed_results = []

    for result in results.get("results", []):
        parsed_result = {
            "title": result.get("title"),
            "url": result.get("url"),
            "content": result.get("content"),
            "score": result.get("score"),
        }

        if "published_date" in result:
            parsed_result["published_date"] = result["published_date"]

        parsed_results.append(parsed_result)

    return parsed_results
