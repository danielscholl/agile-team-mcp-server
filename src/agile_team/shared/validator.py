"""Input validator for the model wrapper MCP server."""

import os
import logging
from typing import List, Dict, Tuple, Any
from mcp.server.fastmcp.exceptions import ValidationError
from agile_team.shared.utils import parse_provider_model, weak_provider_and_model, SHORT_NAME_MAPPING

# Configure logging
logger = logging.getLogger(__name__)

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
            
            logger.info(f"Model correction: {provider}:{original_model} -> {provider}:{model}")
        
        validated_models.append((provider, model))
    
    return validated_models


def validate_models_prefixed_by_provider(models_prefixed_by_provider: List[str]) -> bool:
    """
    Validate model strings in the format "provider:model".
    
    Args:
        models_prefixed_by_provider: List of strings in format "provider:model"
        
    Returns:
        True if all models are valid, raises ValueError otherwise
    """
    if not models_prefixed_by_provider:
        raise ValueError("No models specified")
    
    from agile_team.shared.model_router import list_providers
    valid_providers = list_providers()
    
    for entry in models_prefixed_by_provider:
        if ":" not in entry:
            raise ValueError(f"Invalid model format: {entry}. Expected 'provider:model'")
        
        provider, model = entry.split(":", 1)
        if not provider or not model:
            raise ValueError(f"Invalid model format: {entry}. Provider and model cannot be empty")
        
        # Check if provider is valid
        normalized_provider = provider.lower()
        if normalized_provider not in valid_providers:
            raise ValueError(f"Invalid provider: {provider}")
    
    return True


def validate_provider(provider: str) -> bool:
    """
    Validate provider name.
    
    Args:
        provider: Provider name or shorthand
        
    Returns:
        True if provider is valid, raises ValueError otherwise
    """
    if not provider:
        raise ValueError("Provider cannot be empty")
    
    from agile_team.shared.model_router import list_providers
    valid_providers = list_providers()
    
    normalized_provider = provider.lower()
    if normalized_provider not in valid_providers:
        raise ValueError(f"Invalid provider: {provider}")
    
    return True


def validate_provider_api_keys() -> Dict[str, bool]:
    """
    Validate that API keys are available for each provider.
    
    Returns:
        Dictionary mapping provider names to availability status (True/False)
    """
    from agile_team.shared.model_router import PROVIDER_CONFIG
    
    availability = {}
    
    for provider, config in PROVIDER_CONFIG.items():
        if provider == "ollama":
            # Ollama is local and doesn't need an API key
            availability[provider] = True
        elif "key_env" in config:
            # Check if the API key is available
            api_key = os.environ.get(config["key_env"])
            availability[provider] = bool(api_key)
        else:
            # No API key required
            availability[provider] = True
    
    return availability


def print_provider_availability(detailed: bool = False) -> None:
    """
    Print information about which providers are available based on API keys.
    
    Args:
        detailed: Whether to print detailed information
    """
    # Import here to avoid circular imports
    from agile_team.shared.model_router import PROVIDER_CONFIG
    
    availability = validate_provider_api_keys()
    
    # Get available providers
    available = [p for p, status in availability.items() if status]
    unavailable = [p for p, status in availability.items() if not status]
    
    # Map to include short names
    provider_aliases = {
        "openai": "o",
        "anthropic": "a",
        "gemini": "g",
        "deepseek": "d",
        "groq": "q",
        "ollama": "l",
    }
    
    # Format available providers with aliases
    available_list = []
    for p in available:
        if p in provider_aliases:
            available_list.append(f"{p} [{provider_aliases[p]}]")
        else:
            available_list.append(p)
    
    # Log available providers
    if available:
        logger.info(f"Available LLM providers: {', '.join(available_list)}")
    else:
        logger.warning("No LLM providers are available. Please check your API keys.")
    
    # Log unavailable providers if detailed
    if detailed and unavailable:
        logger.warning(f"The following providers are unavailable due to missing API keys: {', '.join(unavailable)}")
        logger.warning("To use these providers, please set the following environment variables:")
        
        for p in unavailable:
            if p in PROVIDER_CONFIG and "key_env" in PROVIDER_CONFIG[p]:
                logger.warning(f"  - {PROVIDER_CONFIG[p]['key_env']} for {p}")