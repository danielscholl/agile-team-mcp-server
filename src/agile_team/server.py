"""MCP Server implementation for Agile Team."""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Optional

# Import tools
from agile_team.tools.prompt import prompt
from agile_team.tools.prompt_from_file import prompt_from_file
from agile_team.tools.prompt_from_file_to_file import prompt_from_file_to_file
from agile_team.tools.list_providers import list_providers
from agile_team.tools.list_models import list_models
from agile_team.tools.persona_dm import persona_dm, DEFAULT_PERSONA_PROMPT
from agile_team.tools.persona_ba import persona_ba, DEFAULT_BA_PROMPT, DEFAULT_BA_DECISION_PROMPT

# Import centralized configuration
from agile_team.shared.config import DEFAULT_MODEL, DEFAULT_TEAM_MODELS, DEFAULT_DECISION_MAKER_MODEL

# Default model for prompt tools (maintained for backward compatibility)
DEFAULT_PROMPT_MODEL = [DEFAULT_MODEL]

# Create a FastMCP server instance
mcp = FastMCP("Agile Team MCP Server")

# Register tools using decorators
@mcp.tool()
def prompt_tool(text: str, models_prefixed_by_provider: List[str] = None) -> List[str]:
    """
    Send a text prompt to multiple LLM models and return their responses.
    
    Args:
        text: The prompt text to send to the models
        models_prefixed_by_provider: List of models in format "provider:model" (e.g., "openai:gpt-4").
                                     If None, defaults to ["openai:gpt-4o-mini"]
    
    Returns:
        List of responses, one from each specified model
    """
    if models_prefixed_by_provider is None:
        models_prefixed_by_provider = DEFAULT_PROMPT_MODEL
    return prompt(text, models_prefixed_by_provider)


@mcp.tool()
def prompt_from_file_tool(file_path: str, models_prefixed_by_provider: List[str] = None) -> List[str]:
    """
    Read a prompt from a file and send it to multiple LLM models.
    
    Args:
        file_path: Path to the file containing the prompt text
        models_prefixed_by_provider: List of models in format "provider:model" (e.g., "openai:gpt-4").
                                     If None, defaults to ["openai:gpt-4o-mini"]
    
    Returns:
        List of responses, one from each specified model
    """
    if models_prefixed_by_provider is None:
        models_prefixed_by_provider = DEFAULT_PROMPT_MODEL
    return prompt_from_file(file_path, models_prefixed_by_provider)


@mcp.tool()
def prompt_from_file2file_tool(
    file_path: str, models_prefixed_by_provider: List[str] = None, output_dir: str = None, 
    output_extension: str = None, output_path: str = None
) -> List[str]:
    """
    Read a prompt from a file, send it to multiple LLM models, and write responses to files.
    
    Args:
        file_path: Path to the file containing the prompt text
        models_prefixed_by_provider: List of models in format "provider:model" (e.g., "openai:gpt-4").
                                     If None, defaults to ["openai:gpt-4o-mini"]
        output_dir: Directory where response files should be saved (defaults to input file's directory/responses)
        output_extension: File extension for output files (e.g., 'py', 'txt', 'md')
                          If None, defaults to 'md' (default: None)
        output_path: Optional full output path with filename. If provided, the extension
                     from this path will be used (overrides output_extension).
    
    Returns:
        List of file paths where responses were written
    """
    if models_prefixed_by_provider is None:
        models_prefixed_by_provider = DEFAULT_PROMPT_MODEL
    return prompt_from_file_to_file(file_path, models_prefixed_by_provider, output_dir, output_extension, output_path)


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


@mcp.tool()
def persona_dm_tool(
    from_file: str,
    models_prefixed_by_provider: Optional[List[str]] = None,
    output_dir: Optional[str] = None,
    output_extension: Optional[str] = None,
    output_path: Optional[str] = None,
    persona_dm_model: str = DEFAULT_DECISION_MAKER_MODEL, 
    persona_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
    """
    Generate responses from multiple LLM models and use a decision maker model to choose the best direction.
    
    This tool first sends a prompt from a file to multiple models, then uses a designated
    decision maker model to evaluate all responses and provide a final decision.
    
    Args:
        from_file: Path to the file containing the prompt text
        models_prefixed_by_provider: List of team member models in format "provider:model" 
                                    (if None, defaults to ["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"])
        output_dir: Directory where response files should be saved (defaults to input file's directory/responses)
        output_extension: File extension for output files (e.g., 'py', 'txt', 'md')
        output_path: Optional full output path with filename for the persona document
        persona_dm_model: Model to use for making the decision (defaults to DEFAULT_DECISION_MAKER_MODEL)
        persona_prompt: Custom persona prompt template (if None, uses the default)
    
    Returns:
        Path to the persona output file
    """
    return persona_dm(
        from_file=from_file,
        models_prefixed_by_provider=models_prefixed_by_provider,
        output_dir=output_dir,
        output_extension=output_extension,
        output_path=output_path,
        persona_dm_model=persona_dm_model,
        persona_prompt=persona_prompt
    )


@mcp.tool()
def persona_ba_tool(
    from_file: str,
    models_prefixed_by_provider: Optional[List[str]] = None,
    output_dir: Optional[str] = None,
    output_extension: Optional[str] = None,
    output_path: Optional[str] = None,
    use_decision_maker: bool = False,
    decision_maker_models: Optional[List[str]] = None,
    ba_prompt: str = DEFAULT_BA_PROMPT,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_BA_DECISION_PROMPT
) -> str:
    """
    Generate business analysis using a specialized Business Analyst persona, with optional decision making.
    
    This tool uses a specialized Business Analyst prompt to analyze business requirements
    from a file. It can either use a single model or leverage the team decision-making
    functionality to get multiple perspectives and consolidate them.
    
    Args:
        from_file: Path to the file containing the business requirements
        models_prefixed_by_provider: List of models in format "provider:model"
                                    (if None, defaults to DEFAULT_MODEL)
        output_dir: Directory where response files should be saved (defaults to input file's directory/responses)
        output_extension: File extension for output files (e.g., 'py', 'txt', 'md')
        output_path: Optional full output path with filename for the output document
        use_decision_maker: Whether to use the decision maker functionality
        decision_maker_models: Models to use if use_decision_maker is True
                             (if None, defaults to DEFAULT_TEAM_MODELS)
        ba_prompt: Custom business analyst prompt template
        decision_maker_model: Model to use for decision making (defaults to DEFAULT_DECISION_MAKER_MODEL)
        decision_maker_prompt: Custom persona prompt template for decision making
    
    Returns:
        Path to the business analysis output file
    """
    return persona_ba(
        from_file=from_file,
        models_prefixed_by_provider=models_prefixed_by_provider,
        output_dir=output_dir,
        output_extension=output_extension,
        output_path=output_path,
        use_decision_maker=use_decision_maker,
        decision_maker_models=decision_maker_models,
        ba_prompt=ba_prompt,
        decision_maker_model=decision_maker_model,
        decision_maker_prompt=decision_maker_prompt
    )