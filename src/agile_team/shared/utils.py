"""Utility functions for the Agile Team MCP Server."""

import os
from typing import Dict, List, Tuple, Optional
from mcp.server.fastmcp.exceptions import ValidationError, ToolError, ResourceError
import json

# Mapping of short provider names to full provider names
SHORT_NAME_MAPPING = {
    "o": "openai",
    "a": "anthropic",
    "g": "google",
    "d": "deepseek",
    "q": "groq",
    "l": "ollama"
}


def format_error_response(error_code: str, error_message: str, details: Dict = None) -> Dict:
    """Format a standard error response."""
    response = {
        "error": {
            "code": error_code,
            "message": error_message
        }
    }
    if details:
        response["error"]["details"] = details
    return response


def validate_file_exists(file_path: str) -> None:
    """Validate that a file exists."""
    if not os.path.isfile(file_path):
        raise ResourceError(f"File not found: {file_path}")


def validate_directory_exists(dir_path: str) -> None:
    """Validate that a directory exists and create it if it doesn't."""
    if not os.path.isdir(dir_path):
        try:
            os.makedirs(dir_path, exist_ok=True)
        except Exception as e:
            raise ResourceError(f"Failed to create directory {dir_path}: {str(e)}")


def read_file(file_path: str) -> str:
    """Read a file and return its contents."""
    validate_file_exists(file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise ResourceError(f"Failed to read file {file_path}: {str(e)}")


def write_file(file_path: str, content: str) -> None:
    """Write content to a file."""
    directory = os.path.dirname(file_path)
    if directory:
        validate_directory_exists(directory)
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise ResourceError(f"Failed to write to file {file_path}: {str(e)}")


def parse_provider_model(provider_model: str) -> Tuple[str, str]:
    """Parse a provider:model string into provider and model components."""
    if ":" not in provider_model:
        raise ValidationError(f"Invalid format: {provider_model}. Expected format: provider:model")
    
    provider, model = provider_model.split(":", 1)
    if not provider or not model:
        raise ValidationError(f"Invalid format: {provider_model}. Provider and model cannot be empty")
    
    return provider, model


def weak_provider_and_model(provider: str, model: str, available_models: List[str]) -> Tuple[str, str]:
    """
    Attempt to correct provider and model names using fuzzy matching.
    
    Args:
        provider: The provider name to correct
        model: The model name to correct
        available_models: A list of available models for the provider
        
    Returns:
        Tuple of corrected (provider, model)
    """
    # Map of provider name variations with only single-letter shortcuts
    provider_map = {
        "openai": ["openai", "o"],
        "anthropic": ["anthropic", "a"],
        "google": ["google", "g"],
        "deepseek": ["deepseek", "d"],
        "groq": ["groq", "q"],
        "ollama": ["ollama", "l"],
    }
    
    # Try to find the correct provider
    normalized_provider = provider.lower()
    corrected_provider = None
    
    for key, variations in provider_map.items():
        if normalized_provider in variations:
            corrected_provider = key
            break
    
    # If we couldn't correct the provider, use the original
    if not corrected_provider:
        corrected_provider = provider
        
    # If the model is not in the available models, try fuzzy matching
    if model not in available_models:
        # Look for partial matches
        for available_model in available_models:
            if model.lower() in available_model.lower() or available_model.lower() in model.lower():
                return corrected_provider, available_model
                
        # If no matches, use the first available model as a fallback
        if available_models:
            return corrected_provider, available_models[0]
    
    return corrected_provider, model