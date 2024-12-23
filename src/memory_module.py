import uuid
from typing import Any, Dict, List, Optional

from loguru import logger
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from qdrant_client.http.models import Distance

openai_client = OpenAI()


def my_embedding_function(text: str) -> List[float]:
    response = openai_client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding


class MemoryModule:
    def __init__(
        self,
        collection_name: str = "agent_memory",
        host: str = "localhost",
        port: int = 6333,
        vector_size: int = 768,
    ):
        """
        Initializes the connection to Qdrant and ensures that
        the specified collection exists.
        """
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.vector_size = vector_size

        # Create collection if not exists
        try:
            self.client.get_collection(collection_name)
            logger.info(f"Collection '{collection_name}' already exists in Qdrant.")
        except Exception:
            logger.info(f"Creating collection '{collection_name}' in Qdrant.")
            self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config=qdrant_models.VectorParams(
                    size=vector_size, distance=Distance.COSINE
                ),
            )

    def store(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Embed the content and store it in Qdrant with optional metadata.
        """
        embedding = my_embedding_function(content)
        point_id = str(uuid.uuid4())  # unique identifier
        vector = embedding

        payload = {"content": content}
        if metadata:
            payload.update(metadata)

        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    qdrant_models.PointStruct(
                        id=point_id,
                        vector=vector,
                        payload=payload,
                    )
                ],
            )
            logger.info(f"Stored memory in Qdrant: {point_id}")
        except Exception as e:
            logger.error(f"Error storing memory: {e}")

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search the memory by embedding the query and retrieving the top_k most similar points.
        Returns a list of payloads with content/metadata.
        """
        query_vector = my_embedding_function(query)
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
            )
            # search_result is a list of ScoredPoint objects
            results = []
            for scored_point in search_result:
                results.append(
                    {
                        "content": scored_point.payload.get("content", "")
                        if scored_point.payload
                        else "",
                        "metadata": {
                            k: v for k, v in (scored_point.payload or {}).items() if k != "content"
                        },
                        "score": scored_point.score,
                    }
                )
            return results
        except Exception as e:
            logger.error(f"Error searching memory: {e}")
            return []
