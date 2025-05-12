"""Model router for the Agile Team MCP Server."""

import os
from typing import Dict, List, Tuple, Optional, Any
from mcp.server.fastmcp.exceptions import ValidationError, ToolError, ResourceError
import json
import importlib
from dotenv import load_dotenv
from agile_team.shared.utils import SHORT_NAME_MAPPING

# Load environment variables
load_dotenv()

# Supported providers and their import paths
PROVIDER_MODULES = {
    "openai": {
        "module": "openai",
        "key_env": "OPENAI_API_KEY",
        "models": [
            "gpt-4o",
            "gpt-4o-mini", 
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ]
    },
    "anthropic": {
        "module": "anthropic",
        "key_env": "ANTHROPIC_API_KEY",
        "models": [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20241022"
        ]
    },
    "google": {
        "module": "google.generativeai",
        "key_env": "GOOGLE_API_KEY",
        "models": [
            "gemini-1.5-pro-latest",
            "gemini-1.5-flash-latest", 
            "gemini-1.0-pro"
        ]
    },
    "deepseek": {
        "module": "openai", # Using OpenAI client with different base URL
        "key_env": "DEEPSEEK_API_KEY",
        "models": [
            "deepseek-coder",
            "deepseek-chat"
        ],
        "base_url": "https://api.deepseek.com/v1"
    },
    "groq": {
        "module": "openai", # Using OpenAI client with different base URL
        "key_env": "GROQ_API_KEY",
        "models": [
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ],
        "base_url": "https://api.groq.com/openai/v1"
    },
    "ollama": {
        "module": "ollama",
        "models": [
            "llama3",
            "mistral",
            "phi3"
        ],
        "local": True
    }
}


# Initialized clients for different providers
_clients = {}


def _initialize_client(provider: str) -> Any:
    """Initialize a client for the given provider."""
    # If the provider is a single-letter code, convert it to full name
    if provider in SHORT_NAME_MAPPING:
        provider = SHORT_NAME_MAPPING[provider]

    if provider in _clients:
        return _clients[provider]

    if provider not in PROVIDER_MODULES:
        raise ValidationError(f"Unsupported provider: {provider}")

    provider_info = PROVIDER_MODULES[provider]
    
    # For local providers like Ollama, no API key needed
    if provider_info.get("local", False):
        try:
            module = importlib.import_module(provider_info["module"])
            _clients[provider] = module
            return module
        except ImportError:
            raise ResourceError(f"Provider {provider} requires the {provider_info['module']} package to be installed")
    
    # For cloud providers, check API key
    api_key = os.getenv(provider_info["key_env"])
    if not api_key:
        raise ValidationError(f"Missing API key for {provider}. Set the {provider_info['key_env']} environment variable")
    
    try:
        module = importlib.import_module(provider_info["module"])
        
        if provider == "google":
            # Special handling for Google
            module.configure(api_key=api_key)
            _clients[provider] = module
            return module
            
        elif provider in ["deepseek", "groq"]:
            # For OpenAI-compatible APIs
            from openai import OpenAI
            client = OpenAI(
                api_key=api_key,
                base_url=provider_info["base_url"]
            )
            _clients[provider] = client
            return client
            
        elif provider == "anthropic":
            # For Anthropic
            client = module.Anthropic(api_key=api_key)
            _clients[provider] = client
            return client
            
        else:
            # Default for OpenAI
            client = module.OpenAI(api_key=api_key)
            _clients[provider] = client
            return client
            
    except ImportError:
        raise ResourceError(f"Provider {provider} requires the {provider_info['module']} package to be installed")
    except Exception as e:
        raise ResourceError(f"Failed to initialize client for {provider}: {str(e)}")


def get_client(provider: str) -> Any:
    """Get a client for the given provider."""
    return _initialize_client(provider)


def list_providers(detailed: bool = False) -> List[str] | Dict[str, List[str]]:
    """
    List all supported providers.

    Args:
        detailed: If True, returns a dictionary mapping providers to their aliases.
                 If False, returns a flat list of all providers and aliases.

    Returns:
        Either a list of all provider names and aliases (if detailed=False),
        or a dictionary mapping each provider to its aliases (if detailed=True)
    """
    # Main providers
    main_providers = list(PROVIDER_MODULES.keys())

    # Add short names only
    provider_aliases = {
        "openai": ["o"],
        "anthropic": ["a"],
        "google": ["g"],
        "deepseek": ["d"],
        "groq": ["q"],
        "ollama": ["l"],
    }

    if detailed:
        return provider_aliases
    else:
        all_providers = main_providers.copy()
        for provider, aliases in provider_aliases.items():
            all_providers.extend(aliases)
        return all_providers


def list_models(provider: str) -> List[str]:
    """List all models for the given provider."""
    # Normalize provider name
    from agile_team.shared.utils import weak_provider_and_model

    # If the provider is a single-letter code, convert it to full name
    if provider in SHORT_NAME_MAPPING:
        provider = SHORT_NAME_MAPPING[provider]

    provider_info = None
    for p in PROVIDER_MODULES:
        corrected_provider, _ = weak_provider_and_model(
            provider, "", PROVIDER_MODULES[p].get("models", [])
        )
        if corrected_provider == p:
            provider_info = PROVIDER_MODULES[p]
            break

    if not provider_info:
        raise ValidationError(f"Unsupported provider: {provider}")

    # For most providers, return the static list
    if "models" in provider_info:
        return provider_info["models"]

    # For providers that can dynamically list models, implement that here
    # This is a placeholder - in a real implementation, you would query the API
    return []


def prompt_model(provider: str, model: str, text: str) -> str:
    """Send a prompt to a model and return the response."""
    # If the provider is a single-letter code, convert it to full name
    if provider in SHORT_NAME_MAPPING:
        provider = SHORT_NAME_MAPPING[provider]

    client = get_client(provider)

    try:
        if provider == "openai" or provider in ["deepseek", "groq"]:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": text}],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content

        elif provider == "anthropic":
            response = client.messages.create(
                model=model,
                max_tokens=1000,
                messages=[{"role": "user", "content": text}]
            )
            return response.content[0].text

        elif provider == "google":
            model_obj = client.GenerativeModel(model_name=model)
            response = model_obj.generate_content(text)
            return response.text

        elif provider == "ollama":
            response = client.chat(
                model=model,
                messages=[{"role": "user", "content": text}]
            )
            return response["message"]["content"]

        else:
            raise ValidationError(f"Unsupported provider: {provider}")

    except Exception as e:
        raise ToolError(f"Error from {provider} API: {str(e)}")