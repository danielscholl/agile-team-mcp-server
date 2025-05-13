"""Model router for the Agile Team MCP Server."""

import os
import importlib
import logging
from typing import Dict, List, Any, Optional, Union
from mcp.server.fastmcp.exceptions import ValidationError, ToolError, ResourceError
from dotenv import load_dotenv
from agile_team.shared.utils import weak_provider_and_model
from agile_team.shared.data_types import ModelProviders

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Provider configuration based on the ModelProviders enum
PROVIDER_CONFIG = {}

# Populate provider configuration dynamically from the ModelProviders enum
for provider in ModelProviders:
    if provider.full_name == "testing":
        # Special configuration for testing provider
        PROVIDER_CONFIG[provider.full_name] = {
            "module_path": "agile_team.shared.llm_providers.testing",
            "models": ["model1", "model2", "test-model"],
            "testing": True  # Flag to identify this as a testing provider
        }
    elif provider.full_name == "ollama":
        # Special configuration for local providers
        PROVIDER_CONFIG[provider.full_name] = {
            "module_path": f"agile_team.shared.llm_providers.{provider.full_name}",
            "models": [
                "llama3",
                "mistral",
                "phi3"
            ],
            "local": True
        }
    else:
        # Standard configuration for cloud providers
        PROVIDER_CONFIG[provider.full_name] = {
            "module_path": f"agile_team.shared.llm_providers.{provider.full_name}",
            "key_env": f"{provider.full_name.upper()}_API_KEY"
        }

# Add specific models for each provider
PROVIDER_CONFIG["openai"]["models"] = [
    "gpt-4o",
    "gpt-4o-mini", 
    "gpt-4-turbo",
    "gpt-3.5-turbo"
]

PROVIDER_CONFIG["anthropic"]["models"] = [
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-3-5-sonnet-20241022",
    "claude-3-7-sonnet-20250219"
]

PROVIDER_CONFIG["gemini"]["models"] = [
    "gemini-2.5-pro-preview-03-25",
    "gemini-2.5-flash-preview-04-17",
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash-latest", 
    "gemini-1.0-pro"
]

PROVIDER_CONFIG["deepseek"]["models"] = [
    "deepseek-coder",
    "deepseek-chat",
    "deepseek-reasoner",
    "deepseek-coder-v2",
    "deepseek-reasoner-lite"
]

PROVIDER_CONFIG["groq"]["models"] = [
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
    "llama-3.1-70b-versatile",
    "llama-3.3-70b-versatile"
]


class ModelRouter:
    """Router for model operations across different providers."""
    
    @staticmethod
    def _get_provider_module(provider: str) -> Any:
        """
        Get or import the provider module.
        
        Args:
            provider: Provider name
            
        Returns:
            Provider module
        """
        # Convert provider name to full name using ModelProviders enum
        provider_enum = ModelProviders.from_name(provider)
        if not provider_enum:
            raise ValidationError(f"Unsupported provider: {provider}")
            
        provider = provider_enum.full_name
        if provider not in PROVIDER_CONFIG:
            raise ValidationError(f"Provider {provider} not configured in PROVIDER_CONFIG")
            
        provider_info = PROVIDER_CONFIG[provider]
        
        # For testing providers, no API key needed
        if provider_info.get("testing", False):
            logger.debug(f"Using testing provider: {provider}")
        # For local providers like Ollama, no API key needed
        elif provider_info.get("local", False):
            # Check if OLLAMA_HOST is set (not required but recommended)
            if provider == "ollama" and not os.getenv("OLLAMA_HOST"):
                logger.warning("OLLAMA_HOST environment variable not set, using default")
        else:
            # For cloud providers, check API key
            api_key = os.getenv(provider_info["key_env"])
            if not api_key:
                raise ValidationError(f"Missing API key for {provider}. Set the {provider_info['key_env']} environment variable")
        
        # Import provider module (fresh import each time to avoid test interference)
        try:
            module = importlib.import_module(provider_info["module_path"])
            return module
        except ImportError:
            raise ResourceError(f"Provider module for {provider} not found: {provider_info['module_path']}")
        except Exception as e:
            raise ResourceError(f"Failed to import provider module for {provider}: {str(e)}")

    @staticmethod
    def prompt_model(provider: str, model: str, text: str) -> str:
        """
        Send a prompt to a model and return the response.
        
        Args:
            provider: Provider name
            model: Model name
            text: Prompt text
            
        Returns:
            Model response
        """
        # Convert provider name to full name using ModelProviders enum
        provider_enum = ModelProviders.from_name(provider)
        if not provider_enum:
            raise ValidationError(f"Unsupported provider: {provider}")
        
        provider = provider_enum.full_name
        
        # Get provider module
        provider_module = ModelRouter._get_provider_module(provider)
        
        try:
            # Call the prompt function in the provider module
            return provider_module.prompt(text=text, model=model)
        except Exception as e:
            raise ToolError(f"Error from {provider} API: {str(e)}")

    @staticmethod
    def list_providers(detailed: bool = False) -> Union[List[str], Dict[str, List[str]]]:
        """
        List all supported providers.
    
        Args:
            detailed: If True, returns a dictionary mapping providers to their aliases.
                     If False, returns a flat list of all providers and aliases.
    
        Returns:
            Either a list of all provider names and aliases (if detailed=False),
            or a dictionary mapping each provider to its aliases (if detailed=True)
        """
        # Use ModelProviders enum to build provider information
        provider_aliases = {}
        for provider in ModelProviders:
            # Skip testing provider in production lists unless we're in a test environment
            if provider.full_name == "testing" and os.getenv("TEST_MODE") != "1":
                continue
                
            provider_aliases[provider.full_name] = [provider.short_name]
            
        if detailed:
            return provider_aliases
        else:
            all_providers = list(provider_aliases.keys())
            for provider, aliases in provider_aliases.items():
                all_providers.extend(aliases)
            return all_providers

    @staticmethod
    def list_models(provider: str) -> List[str]:
        """
        List all models for the given provider.
        
        Args:
            provider: Provider name
            
        Returns:
            List of model names
        """
        # Normalize provider name using ModelProviders enum
        provider_enum = ModelProviders.from_name(provider)
        if not provider_enum:
            raise ValidationError(f"Unsupported provider: {provider}")
            
        provider = provider_enum.full_name
        
        # Find the provider in the config
        if provider not in PROVIDER_CONFIG:
            raise ValidationError(f"Provider {provider} not configured in PROVIDER_CONFIG")
            
        provider_info = PROVIDER_CONFIG[provider]
        
        try:
            # Get provider module
            provider_module = ModelRouter._get_provider_module(provider)
            
            # Try to get dynamic list of models from the provider module
            return provider_module.list_models()
        except (AttributeError, ImportError, Exception) as e:
            logger.warning(f"Failed to get dynamic model list for {provider}: {str(e)}")
            logger.info(f"Using static model list for {provider}")
            
            # Fall back to static list if dynamic listing fails
            if "models" in provider_info:
                return provider_info["models"]
            
            # If no static list, return empty list
            logger.warning(f"No models configured for provider {provider} and failed to get dynamic list")
            return []


# Function wrappers to maintain backwards compatibility
def _get_provider_module(provider: str) -> Any:
    """Wrapper for ModelRouter._get_provider_module"""
    return ModelRouter._get_provider_module(provider)


def prompt_model(provider: str, model: str, text: str) -> str:
    """Wrapper for ModelRouter.prompt_model"""
    return ModelRouter.prompt_model(provider, model, text)


def list_providers(detailed: bool = False) -> Union[List[str], Dict[str, List[str]]]:
    """Wrapper for ModelRouter.list_providers"""
    return ModelRouter.list_providers(detailed)


def list_models(provider: str) -> List[str]:
    """Wrapper for ModelRouter.list_models"""
    return ModelRouter.list_models(provider)