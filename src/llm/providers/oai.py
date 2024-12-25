from typing import Dict, List

import openai
from loguru import logger

from src.core.config import settings
from src.core.exceptions import LLMError


async def call_openai(messages: List[Dict[str, str]], **kwargs) -> str:
    """
    Call the OpenAI ChatCompletion endpoint.

    Args:
        messages: A list of dicts with 'role' and 'content'.
        kwargs: Additional parameters (e.g., model, temperature).

    Returns:
        str: Response content from OpenAI.
    """
    #: OpenAI client
    openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    model = kwargs.get("model", settings.OPENAI_MODEL)
    temperature = kwargs.get("temperature", 0.2)

    logger.debug(
        f"Calling OpenAI with model={model}, temperature={temperature}, messages={messages}"
    )

    try:
        response = await openai_client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore
            temperature=temperature,
        )
        if not response.choices[0].message.content:
            raise LLMError("No content in OpenAI response")

        content = response.choices[0].message.content.strip()
        logger.debug(f"OpenAI response: {content}")
        return content
    except Exception as e:
        logger.error(f"OpenAI call failed: {e}")
        raise LLMError("Error during OpenAI API call") from e
