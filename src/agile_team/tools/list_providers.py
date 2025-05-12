"""List providers tool implementation."""

from typing import List, Dict
from agile_team.shared.model_router import list_providers as router_list_providers


def list_providers() -> Dict[str, List[str]]:
    """
    List all supported LLM providers with their shortcuts.
    
    Returns:
        Dictionary with formatted provider information
    """
    # Get the detailed mapping of providers to aliases
    provider_mapping = router_list_providers(detailed=True)
    
    # Create a dictionary with clear labels
    result = {
        "main_providers": list(provider_mapping.keys()),
        "shortcuts": []
    }
    
    # Format shortcuts as readable strings
    for provider, shortcuts in provider_mapping.items():
        for shortcut in shortcuts:
            result["shortcuts"].append(f"[{shortcut}] {provider}")
    
    return result