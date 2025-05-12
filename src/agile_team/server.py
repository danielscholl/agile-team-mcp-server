"""MCP Server implementation for Agile Team."""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict

# Import tools
from agile_team.tools.prompt import prompt
from agile_team.tools.prompt_from_file import prompt_from_file
from agile_team.tools.prompt_from_file_to_file import prompt_from_file_to_file
from agile_team.tools.list_providers import list_providers
from agile_team.tools.list_models import list_models

# Create a FastMCP server instance
mcp = FastMCP("Agile Team MCP Server")

# Register tools using decorators
@mcp.tool()
def prompt_tool(text: str, models_prefixed_by_provider: List[str]) -> List[str]:
    """
    Send a text prompt to multiple LLM models and return their responses.
    
    Args:
        text: The prompt text to send to the models
        models_prefixed_by_provider: List of models in format "provider:model" (e.g., "openai:gpt-4")
    
    Returns:
        List of responses, one from each specified model
    """
    return prompt(text, models_prefixed_by_provider)


@mcp.tool()
def prompt_from_file_tool(file: str, models_prefixed_by_provider: List[str]) -> List[str]:
    """
    Read a prompt from a file and send it to multiple LLM models.
    
    Args:
        file: Path to the file containing the prompt text
        models_prefixed_by_provider: List of models in format "provider:model" (e.g., "openai:gpt-4")
    
    Returns:
        List of responses, one from each specified model
    """
    return prompt_from_file(file, models_prefixed_by_provider)


@mcp.tool()
def prompt_from_file_to_file_tool(
    file: str, models_prefixed_by_provider: List[str], output_dir: str = "."
) -> List[str]:
    """
    Read a prompt from a file, send it to multiple LLM models, and write responses to files.
    
    Args:
        file: Path to the file containing the prompt text
        models_prefixed_by_provider: List of models in format "provider:model" (e.g., "openai:gpt-4")
        output_dir: Directory where response files should be saved (default: current directory)
    
    Returns:
        List of file paths where responses were written
    """
    return prompt_from_file_to_file(file, models_prefixed_by_provider, output_dir)


@mcp.tool()
def list_providers_tool() -> Dict[str, List[str]]:
    """
    List all supported LLM providers.

    Returns:
        Dictionary with main providers and their shortcuts clearly formatted
    """
    return list_providers()


@mcp.tool()
def list_models_tool(provider: str) -> List[str]:
    """
    List all available models for a specific provider.
    
    Args:
        provider: The provider to list models for (e.g., "openai", "anthropic")
    
    Returns:
        List of model names available for the specified provider
    """
    return list_models(provider)