import logging
from typing import Dict, List, Optional

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from src.core.config import settings


class LensProtocolTool:
    """Tool for interacting with the Lens Protocol network."""

    def __init__(self):
        self.client: Optional[Client] = None
        self.logger = logging.getLogger(__name__)
        self.profile_id = settings.LENS_PROFILE_ID
        self._initialize_connection()

    def _initialize_connection(self) -> bool:
        """
        Initialize connection to Lens Protocol using settings.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            if not settings.LENS_API_KEY:
                self.logger.error("Lens API key not configured in settings")
                return False

            transport = RequestsHTTPTransport(
                url="https://api-v2.lens.dev", headers={"x-api-key": settings.LENS_API_KEY}
            )
            self.client = Client(transport=transport, fetch_schema_from_transport=True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Lens connection: {str(e)}")
            return False

    def get_profile(self, profile_id: Optional[str] = None) -> Optional[Dict]:
        """
        Retrieve profile information for a given profile ID.

        Args:
            profile_id (Optional[str]): Lens Protocol profile ID. If None, uses default from settings

        Returns:
            Optional[Dict]: Profile information or None if not found
        """
        if not self.client:
            self.logger.error("Client not initialized. Call initialize_connection first.")
            return None

        try:
            profile_id = profile_id or self.profile_id
            if not profile_id:
                self.logger.error("No profile ID provided or configured in settings")
                return None

            query = gql("""
                query Profile($id: ProfileId!) {
                    profile(request: { profileId: $id }) {
                        id
                        handle
                        bio
                        stats {
                            totalFollowers
                            totalFollowing
                        }
                    }
                }
            """)

            result = self.client.execute(query, variable_values={"id": profile_id})
            profile = result["profile"]

            return {
                "id": profile["id"],
                "handle": profile["handle"],
                "bio": profile["bio"],
                "followers": profile["stats"]["totalFollowers"],
                "following": profile["stats"]["totalFollowing"],
            }
        except Exception as e:
            self.logger.error(f"Failed to retrieve profile: {str(e)}")
            return None

    def publish_content(self, content: str, profile_id: Optional[str] = None) -> Optional[Dict]:
        """
        Publish content to the Lens network.

        Args:
            content (str): Content to publish
            profile_id (Optional[str]): Profile ID to publish under. If None, uses default from settings

        Returns:
            Optional[Dict]: Publication details or None if failed
        """
        if not self.client:
            self.logger.error("Client not initialized. Call initialize_connection first.")
            return None

        try:
            profile_id = profile_id or self.profile_id
            if not profile_id:
                self.logger.error("No profile ID provided or configured in settings")
                return None

            mutation = gql("""
                mutation CreatePost($request: CreatePublicPostRequest!) {
                    createPostTypedData(request: $request) {
                        id
                        content
                        createdAt
                    }
                }
            """)

            variables = {"request": {"profileId": profile_id, "content": content}}

            result = self.client.execute(mutation, variable_values=variables)
            publication = result["createPostTypedData"]

            return {
                "id": publication["id"],
                "content": publication["content"],
                "timestamp": publication["createdAt"],
            }
        except Exception as e:
            self.logger.error(f"Failed to publish content: {str(e)}")
            return None

    def fetch_content(self, query_params: Dict) -> List[Dict]:
        """
        Fetch content from the Lens network based on query parameters.

        Args:
            query_params (dict): Parameters for content query (e.g., orderBy, limit)

        Returns:
            List[Dict]: List of publications matching the query
        """
        if not self.client:
            self.logger.error("Client not initialized. Call initialize_connection first.")
            return []

        try:
            query = gql("""
                query ExplorePublications($request: ExplorePublicationRequest!) {
                    explorePublications(request: $request) {
                        items {
                            ... on Post {
                                id
                                profile {
                                    id
                                }
                                metadata {
                                    content
                                }
                                createdAt
                                stats {
                                    totalAmountOfComments
                                    totalAmountOfMirrors
                                    totalAmountOfReactions
                                }
                            }
                        }
                    }
                }
            """)

            result = self.client.execute(query, variable_values={"request": query_params})
            publications = result["explorePublications"]["items"]

            return [
                {
                    "id": pub["id"],
                    "profile_id": pub["profile"]["id"],
                    "content": pub["metadata"]["content"],
                    "timestamp": pub["createdAt"],
                    "stats": {
                        "comments": pub["stats"]["totalAmountOfComments"],
                        "mirrors": pub["stats"]["totalAmountOfMirrors"],
                        "reactions": pub["stats"]["totalAmountOfReactions"],
                    },
                }
                for pub in publications
            ]
        except Exception as e:
            self.logger.error(f"Failed to fetch content: {str(e)}")
            return []
