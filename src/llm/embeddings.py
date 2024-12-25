from typing import List, Union

import numpy as np
from loguru import logger
from openai import AsyncOpenAI

from src.core.config import settings
from src.llm.llm import get_oai_client


class EmbeddingGenerator:
    """A class to generate embeddings using OpenAI's text embedding models."""

    def __init__(
        self,
        client: AsyncOpenAI = get_oai_client(),
        model: str = settings.OPENAI_EMBEDDING_MODEL,
    ):
        """
        Initialize the embedding generator.

        Args:
            client: AsyncOpenAI client instance
            model: The OpenAI model to use for embeddings
        """
        self.client = client
        self.model = model

    async def get_embedding(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Get embeddings for a single text or list of texts.

        Args:
            text: Single string or list of strings to get embeddings for

        Returns:
            numpy array of embeddings

        Raises:
            ValueError: If input text is empty
            Exception: For API or processing errors
        """
        if not text:
            raise ValueError("Input text cannot be empty")

        # Convert single string to list for consistent handling
        texts = [text] if isinstance(text, str) else text

        try:
            logger.debug(f"Getting embeddings for {len(texts)} texts")
            response = await self.client.embeddings.create(model=self.model, input=texts)

            # Extract embeddings from response
            embeddings = [data.embedding for data in response.data]
            return np.array(embeddings)

        except Exception as e:
            logger.error(f"Error getting embeddings: {str(e)}")
            raise
