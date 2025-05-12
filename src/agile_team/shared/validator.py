"""Input validator for the model wrapper MCP server."""

from typing import List, Tuple
from mcp.server.fastmcp.exceptions import ValidationError
from agile_team.shared.utils import parse_provider_model, weak_provider_and_model


def validate_and_correct_models(models_prefixed_by_provider: List[str]) -> List[Tuple[str, str]]:
    """
    Validate and correct model/provider combinations.
    
    Args:
        models_prefixed_by_provider: List of strings in format "provider:model"
        
    Returns:
        List of tuples containing (provider, model) pairs
    """
    if not models_prefixed_by_provider:
        raise ValidationError("No models specified")
    
    validated_models = []
    
    # Import here to avoid circular imports
    from agile_team.shared.model_router import list_models
    
    for entry in models_prefixed_by_provider:
        # Parse provider and model
        try:
            provider, model = parse_provider_model(entry)
        except ValidationError as e:
            raise ValidationError(f"Invalid model format: {entry}. Expected 'provider:model'")
        
        # Get available models for this provider
        try:
            available_models = list_models(provider)
        except Exception:
            # If the provider is invalid, attempt to correct it
            provider, _ = weak_provider_and_model(provider, model, [])
            try:
                available_models = list_models(provider)
            except Exception as e:
                raise ValidationError(f"Invalid provider: {provider}")
        
        # Check if the model exists or needs correction
        if model not in available_models:
            original_model = model
            _, model = weak_provider_and_model(provider, model, available_models)
            
            print(f"Model correction: {provider}:{original_model} -> {provider}:{model}")
        
        validated_models.append((provider, model))
    
    return validated_models