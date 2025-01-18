"""Spotify integration tool for Nevron."""

import base64
from typing import Dict, List
from urllib.parse import urlencode

import aiohttp
from loguru import logger

from src.core.config import settings
from src.core.exceptions import SpotifyError


class SpotifyTool:
    """Tool for interacting with Spotify's Web API."""

    def __init__(self):
        """Initialize Spotify tool with base configuration."""
        self.base_url = "https://api.spotify.com/v1"
        self.auth_url = "https://accounts.spotify.com/api/token"
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET

    async def authenticate(self) -> str:
        """
        Authenticate with Spotify using Client Credentials flow.

        Returns:
            str: Access token for API requests.

        Raises:
            SpotifyError: If authentication fails.
        """
        try:
            # Create base64 encoded auth string
            auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

            headers = {
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            data = {"grant_type": "client_credentials"}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.auth_url, headers=headers, data=data, ssl=False
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    logger.debug("Successfully authenticated with Spotify")
                    return result["access_token"]
        except Exception as e:
            logger.error(f"Spotify authentication failed: {e}")
            raise SpotifyError(f"Failed to authenticate with Spotify: {e}")

    async def get_user_playlists(self, access_token: str) -> List[Dict]:
        """
        Retrieve user's playlists.

        Args:
            access_token (str): Spotify API access token.

        Returns:
            List[Dict]: List of playlist objects.

        Raises:
            SpotifyError: If playlist retrieval fails.
        """
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            url = f"{self.base_url}/me/playlists"

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    logger.debug(f"Retrieved {len(result['items'])} playlists")
                    return result["items"]
        except Exception as e:
            logger.error(f"Failed to get playlists: {e}")
            raise SpotifyError(f"Failed to retrieve playlists: {e}")

    async def search_song(self, access_token: str, query: str, limit: int = 1) -> List[Dict]:
        """
        Search for songs by name or artist.

        Args:
            access_token (str): Spotify API access token.
            query (str): Search query.
            limit (int): Maximum number of results.

        Returns:
            List[Dict]: List of track objects.

        Raises:
            SpotifyError: If search fails.
        """
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {"q": query, "type": "track", "limit": limit}
            url = f"{self.base_url}/search?{urlencode(params)}"

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, ssl=False) as response:
                    response.raise_for_status()
                    result = await response.json()
                    logger.debug(f"Found {len(result['tracks']['items'])} tracks")
                    return result["tracks"]["items"]
        except Exception as e:
            logger.error(f"Song search failed: {e}")
            raise SpotifyError(f"Failed to search for songs: {e}")

    async def control_playback(self, access_token: str, action: str) -> None:
        """
        Control playback on user's active devices.

        Args:
            access_token (str): Spotify API access token.
            action (str): Playback action ("play", "pause", "skip").

        Raises:
            SpotifyError: If playback control fails.
            ValueError: If action is invalid.
        """
        valid_actions = {"play", "pause", "skip"}
        if action not in valid_actions:
            raise ValueError(f"Invalid action. Must be one of: {valid_actions}")

        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            endpoint = "next" if action == "skip" else action
            url = f"{self.base_url}/me/player/{endpoint}"

            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, ssl=False) as response:
                    response.raise_for_status()
                    logger.debug(f"Successfully executed playback action: {action}")
        except Exception as e:
            logger.error(f"Playback control failed: {e}")
            raise SpotifyError(f"Failed to control playback: {e}")
