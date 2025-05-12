"""Prompt tool implementation."""

from typing import List
from mcp.server.fastmcp.exceptions import ValidationError, ToolError
from agile_team.shared.data_types import PromptRequest
from agile_team.shared.validator import validate_and_correct_models
from agile_team.shared.model_router import prompt_model


def prompt(text: str, models_prefixed_by_provider: List[str]) -> List[str]:
    """
    Send a prompt to multiple models and return their responses.
    
    Args:
        text: The text prompt to send
        models_prefixed_by_provider: List of models in the format "provider:model"
        
    Returns:
        List of responses, one per model
    """
    # Validate request
    request = PromptRequest(text=text, models_prefixed_by_provider=models_prefixed_by_provider)
    
    # Validate and correct models
    validated_models = validate_and_correct_models(request.models_prefixed_by_provider)
    
    # Send prompt to each model
    responses = []
    for provider, model in validated_models:
        try:
            response = prompt_model(provider, model, request.text)
            responses.append(response)
        except Exception as e:
            responses.append(f"Error from {provider}:{model}: {str(e)}")
    
    return responses