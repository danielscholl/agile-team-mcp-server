"""Prompt from file tool implementation."""

from typing import List
from mcp.server.fastmcp.exceptions import ValidationError, ToolError, ResourceError
from agile_team.shared.data_types import FilePromptRequest
from agile_team.shared.validator import validate_and_correct_models
from agile_team.shared.model_router import prompt_model
from agile_team.shared.utils import read_file


def prompt_from_file(file: str, models_prefixed_by_provider: List[str]) -> List[str]:
    """
    Read a prompt from a file and send it to multiple models.
    
    Args:
        file: Path to the file containing the prompt
        models_prefixed_by_provider: List of models in the format "provider:model"
        
    Returns:
        List of responses, one per model
    """
    # Validate request
    request = FilePromptRequest(file=file, models_prefixed_by_provider=models_prefixed_by_provider)
    
    # Read prompt from file
    try:
        prompt_text = read_file(request.file)
    except ResourceError as e:
        raise ResourceError(f"Failed to read prompt file: {str(e)}")
    
    # Validate and correct models
    validated_models = validate_and_correct_models(request.models_prefixed_by_provider)
    
    # Send prompt to each model
    responses = []
    for provider, model in validated_models:
        try:
            response = prompt_model(provider, model, prompt_text)
            responses.append(response)
        except Exception as e:
            responses.append(f"Error from {provider}:{model}: {str(e)}")
    
    return responses