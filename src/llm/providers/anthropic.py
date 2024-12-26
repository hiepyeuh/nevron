from typing import Dict, List

from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic
from loguru import logger

from src.core.config import settings
from src.core.exceptions import LLMError


async def call_anthropic(messages: List[Dict[str, str]], **kwargs) -> str:
    """
    Call the Anthropic Claude API.

    Args:
        messages: A list of dicts with 'role' and 'content'.
        kwargs: Additional parameters (e.g., model, temperature).

    Returns:
        str: Response content from Anthropic.
    """
    #: Anthropic client
    anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    model = kwargs.get("model", settings.ANTHROPIC_MODEL)
    temperature = kwargs.get("temperature", 0.7)

    # Convert `messages` into Anthropic's prompt format
    conversation = ""
    for m in messages:
        if m["role"] == "system":
            conversation += f"(System) {m['content']}\n\n"
        elif m["role"] == "user":
            conversation += f"{HUMAN_PROMPT} {m['content']}\n\n"
        else:
            conversation += f"{AI_PROMPT} {m['content']}\n\n"
    conversation += AI_PROMPT

    logger.debug(f"Calling Anthropic with model={model}, conversation={conversation}")

    try:
        response = anthropic_client.completions.create(
            prompt=conversation,
            model=model,
            temperature=temperature,
            max_tokens_to_sample=1024,
        )
        content = response.completion.strip()
        logger.debug(f"Anthropic response: {content}")
        return content
    except Exception as e:
        logger.error(f"Anthropic call failed: {e}")
        raise LLMError("Error during Anthropic API call") from e
