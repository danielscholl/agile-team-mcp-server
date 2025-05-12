"""List models tool implementation."""

from typing import List
from mcp.server.fastmcp.exceptions import ValidationError
from agile_team.shared.data_types import ProviderRequest
from agile_team.shared.model_router import list_models as router_list_models


def list_models(provider: str) -> List[str]:
    """
    List all models for a given provider.
    
    Args:
        provider: The provider to list models for
        
    Returns:
        List of model names
    """
    # Validate request
    request = ProviderRequest(provider=provider)
    
    try:
        return router_list_models(request.provider)
    except ValidationError as e:
        raise ValidationError(f"Provider not found: {request.provider}")