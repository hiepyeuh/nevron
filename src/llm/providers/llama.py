from pathlib import Path
from typing import Dict, List

import torch
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.core.config import settings
from src.core.exceptions import LLMError


def validate_llama_setup(model_path: str) -> None:
    """
    Validate that the Llama model and tokenizer files exist and are accessible.

    Args:
        model_path: Path to the Llama model directory

    Raises:
        LLMError: If model files are missing or inaccessible
    """
    path = Path(model_path)
    if not path.exists():
        raise LLMError(f"Llama model path does not exist: {model_path}")

    # Check for essential model files
    required_files = ["config.json", "tokenizer.json", "tokenizer_config.json"]
    missing_files = [f for f in required_files if not (path / f).exists()]

    if missing_files:
        raise LLMError(
            f"Missing required Llama model files in {model_path}: {', '.join(missing_files)}"
        )

    # Check for model weights file (either pytorch_model.bin or model.safetensors)
    has_weights = (path / "pytorch_model.bin").exists() or (path / "model.safetensors").exists()
    if not has_weights:
        raise LLMError(
            f"No model weights found in {model_path}. "
            "Expected either pytorch_model.bin or model.safetensors"
        )


async def call_llama(messages: List[Dict[str, str]], **kwargs) -> str:
    """
    Call the Llama model for text generation.

    Args:
        messages: A list of dicts with 'role' and 'content'.
        kwargs: Additional parameters (e.g., model, temperature).

    Returns:
        str: Response content from Llama.

    Raises:
        LLMError: If model loading or inference fails
    """
    model_path = kwargs.get("model_path", settings.LLAMA_MODEL_PATH)
    max_tokens = kwargs.get("max_tokens", settings.LLAMA_MAX_TOKENS)
    temperature = kwargs.get("temperature", 0.7)

    try:
        # Validate model setup before loading
        validate_llama_setup(model_path)

        # Check available memory and adjust device map
        device_map = kwargs.get("device_map", "auto")

        if torch.cuda.is_available():
            gpu_memory = torch.cuda.get_device_properties(0).total_memory
            gpu_memory_gb = gpu_memory / (1024**3)  # Convert to GB

            # Estimate memory requirements based on model size
            model_size = Path(model_path).name.lower()
            required_memory = 0

            if "70b" in model_size:
                required_memory = 140
            elif "405b" in model_size:
                required_memory = 780
            elif "8b" in model_size:
                required_memory = 16

            # Set device based on available memory
            if gpu_memory_gb >= required_memory:
                device_map = "cuda"  # Use GPU if enough memory
            else:
                logger.warning(
                    f"Insufficient GPU memory ({gpu_memory_gb:.1f}GB) for {model_size} model "
                    f"(requires {required_memory}GB). Falling back to CPU."
                )
                device_map = "cpu"
        else:
            logger.info("CUDA not available, using CPU")
            device_map = "cpu"

        # Load model and tokenizer
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_path)
        except Exception as e:
            raise LLMError(f"Failed to load Llama tokenizer: {str(e)}")

        try:
            model = AutoModelForCausalLM.from_pretrained(
                model_path, torch_dtype="auto", device_map=device_map
            )
        except Exception as e:
            raise LLMError(f"Failed to load Llama model: {str(e)}")

        # Format messages into prompt
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"System: {msg['content']}\n"
            elif msg["role"] == "user":
                prompt += f"User: {msg['content']}\n"
            else:
                prompt += f"Assistant: {msg['content']}\n"
        prompt += "Assistant:"

        logger.debug(f"Calling Llama with prompt: {prompt}")

        # Add context window limits based on model size
        model_size = Path(model_path).name.lower()
        if "8b" in model_size:
            max_length = 2048
        elif "70b" in model_size:
            max_length = 4096
        elif "405b" in model_size:
            max_length = 8192
        else:
            max_length = 2048  # Default

        # Generate response
        try:
            inputs = tokenizer(
                prompt, return_tensors="pt", max_length=max_length, truncation=True
            ).to(model.device)
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=kwargs.get("top_p", 0.9),
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            raise LLMError(f"Llama inference failed: {str(e)}")

        # Extract assistant's response
        content = response.split("Assistant:")[-1].strip()
        if not content:
            raise LLMError("Llama generated empty response")

        logger.debug(f"Llama response: {content}")
        return content

    except LLMError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in Llama call: {e}")
        raise LLMError("Error during Llama model inference") from e
