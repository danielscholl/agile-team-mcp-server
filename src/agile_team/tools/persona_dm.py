"""Persona DM (Decision Maker) tool implementation."""

import os
from typing import List, Optional
from mcp.server.fastmcp.exceptions import ValidationError, ToolError, ResourceError
from agile_team.shared.data_types import FileToFilePromptRequest
from agile_team.shared.validator import validate_and_correct_models
from agile_team.shared.model_router import prompt_model
from agile_team.shared.utils import read_file, write_file, validate_directory_exists, load_prompt_file
from agile_team.tools.prompt_from_file_to_file import prompt_from_file_to_file

# Default persona decision model
DEFAULT_PERSONA_DM_MODEL = "openai:o4-mini"

# Default team member models
DEFAULT_TEAM_MODELS = ["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:emini-2.5-pro-preview-03-25"]

# Load prompt from file
DEFAULT_PERSONA_PROMPT = load_prompt_file("dm_prompt.md")


def persona_dm(
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    persona_dm_model: str = DEFAULT_PERSONA_DM_MODEL,
    persona_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
    """
    Generate responses from multiple LLM models and then use a persona decision model to choose the best direction.
    
    Args:
        from_file: Path to the file containing the prompt
        models_prefixed_by_provider: List of models in the format "provider:model" (if None, defaults to ["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"])
        output_dir: Directory where response files should be saved (defaults to input file's directory/responses)
        output_extension: File extension for output files (e.g., '.py', '.txt', '.md')
        output_path: Optional full output path with filename for the persona document
        persona_dm_model: Model to use for making the decision
        persona_prompt: Custom persona prompt template (if None, uses the default)
        
    Returns:
        Path to the persona output file
    """
    # Use default models if none provided, or validate that enough models were provided
    if models_prefixed_by_provider is None:
        models_prefixed_by_provider = DEFAULT_TEAM_MODELS
    elif len(models_prefixed_by_provider) < 2:
        raise ValidationError("At least two team member models must be provided for decision making")
    
    # Handle path parameters based on input
    if output_path and output_dir is None:
        # Extract directory from output_path for team responses
        team_output_dir = os.path.dirname(output_path) or "."
    elif output_dir is None:
        # Use from_file's directory + responses by default
        input_file_dir = os.path.dirname(from_file) or "."
        team_output_dir = os.path.join(input_file_dir, "responses")
    else:
        # Use provided output_dir
        team_output_dir = output_dir
        
    # Ensure the team output directory exists
    os.makedirs(team_output_dir, exist_ok=True)
    
    # First, generate team responses using prompt_from_file_to_file with explicit parameters
    team_responses_files = prompt_from_file_to_file(
        file_path=from_file,
        models_prefixed_by_provider=models_prefixed_by_provider,
        output_dir=team_output_dir,
        output_extension=output_extension
    )
    
    # Read the original prompt from the file
    try:
        original_prompt = read_file(from_file)
    except ResourceError as e:
        raise ResourceError(f"Failed to read prompt file: {str(e)}")
    
    # Read each team member's response from the output files
    team_responses_text = ""
    for response_file in team_responses_files:
        try:
            # Extract the model name from the filename
            file_name = os.path.basename(response_file)
            # Check if this is an error file
            if "_error" in file_name:
                continue
                
            # Extract model info from filename
            model_info = file_name.split('_', 1)[1]  # Remove the prompt file name prefix
            model_info = os.path.splitext(model_info)[0]  # Remove file extension
                
            # Read the response
            response = read_file(response_file)
            
            # Add to the team responses section
            # For backward compatibility - handle both analyst-documents and team-decisions format
            if "<analyst-documents>" in persona_prompt:
                team_responses_text += f"""<analyst-document>
    <model-name>{model_info}</model-name>
    <document>{response}</document>
</analyst-document>
"""
            else:
                team_responses_text += f"""<team-response>
    <model-name>{model_info}</model-name>
    <response>{response}</response>
</team-response>
"""
        except Exception as e:
            # Skip files that can't be read
            continue
    
    # Prepare the persona prompt with the original prompt and team responses
    final_persona_prompt = persona_prompt.format(
        original_prompt=original_prompt,
        team_responses=team_responses_text
    )
    
    # Validate and correct the persona model
    validated_models = validate_and_correct_models([persona_dm_model])
    if not validated_models:
        raise ValidationError(f"Invalid persona model: {persona_dm_model}")
    
    # Extract the provider and model
    provider, model = validated_models[0]
    
    try:
        # Get decision from the persona model
        decision = prompt_model(provider, model, final_persona_prompt)
        
        # Handle the persona output path
        if output_path:
            # Use the exact path specified
            persona_file_path = output_path
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        else:
            # Determine the file extension to use (.md by default)
            extension = ".md"
            if output_extension:
                extension = output_extension if output_extension.startswith(".") else f".{output_extension}"
                
            # Extract base name from prompt file
            base_filename = os.path.basename(from_file)
            file_name, _ = os.path.splitext(base_filename)
            
            # Create the persona output filename
            output_filename = f"{file_name}_persona{extension}"
            persona_file_path = os.path.join(team_output_dir, output_filename)
        
        # Write the decision to the output file
        write_file(persona_file_path, decision)
        
        return persona_file_path
        
    except Exception as e:
        # Handle errors when getting a decision
        error_message = f"Error getting decision from {provider}:{model}: {str(e)}"
        
        # Determine error file path
        if output_path:
            # Create error file next to the specified output path
            dir_path = os.path.dirname(output_path) or "."
            base_name = os.path.basename(output_path)
            name, ext = os.path.splitext(base_name)
            error_file_path = os.path.join(dir_path, f"{name}_error{ext}")
        else:
            # Create standard error file in the team output directory
            base_filename = os.path.basename(from_file)
            file_name, _ = os.path.splitext(base_filename)
            extension = ".md"
            if output_extension:
                extension = output_extension if output_extension.startswith(".") else f".{output_extension}"
            error_file_path = os.path.join(team_output_dir, f"{file_name}_persona_error{extension}")
        
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(error_file_path) or ".", exist_ok=True)
        
        # Write error to file
        write_file(error_file_path, error_message)
        raise ToolError(error_message)