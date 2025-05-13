"""List providers tool implementation."""

from typing import List, Dict
from agile_team.shared.model_router import list_providers as router_list_providers
from agile_team.shared.utils import SHORT_NAME_MAPPING


def list_providers() -> List[Dict[str, str]]:
    """
    List all supported LLM providers with their information.
    
    Returns:
        List of dictionaries with provider information, each containing:
            - name: Uppercase name of the provider (e.g., "OPENAI")
            - full_name: Lowercase name used in API calls (e.g., "openai") 
            - short_name: Single letter alias (e.g., "o")
    """
    # Get the detailed mapping of providers to aliases
    provider_mapping = router_list_providers(detailed=True)
    
    # Create provider information objects
    result = []
    
    # Provider to short name mapping (reverse of SHORT_NAME_MAPPING)
    short_names = {}
    for short, full in SHORT_NAME_MAPPING.items():
        if len(short) == 1:  # Only include single-letter shortcuts
            short_names[full] = short
    
    # Build the provider info list
    for provider in provider_mapping.keys():
        result.append({
            "name": provider.upper(),
            "full_name": provider.lower(),
            "short_name": short_names.get(provider.lower(), "")
        })
    
    return result