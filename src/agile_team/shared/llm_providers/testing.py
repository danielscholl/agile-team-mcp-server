"""
Testing provider implementation.

This provider is specifically designed for testing purposes.
It does not require API keys and returns predictable responses.
"""

import logging
from typing import List

# Configure logging
logger = logging.getLogger(__name__)

def prompt(text: str, model: str) -> str:
    """
    Mock implementation of prompt function for testing.
    
    Args:
        text: The prompt text
        model: The model name
        
    Returns:
        A predictable response based on the input text
    """
    logger.info(f"Testing provider received prompt request for model {model}")
    
    # Return predictable responses based on input text
    if "capital of France" in text:
        return "Paris is the capital of France."
    elif "largest planet" in text:
        return "Jupiter is the largest planet in our solar system."
    elif "test error" in text:
        raise ValueError("Test error triggered by request")
    else:
        return f"Testing response for: {text}"

def list_models() -> List[str]:
    """
    Mock implementation of list_models function for testing.
    
    Returns:
        A predetermined list of test models
    """
    logger.info("Testing provider received list_models request")
    return ["test-model-1", "test-model-2", "test-model-3"]