"""Decision maker tool implementation."""

import os
from typing import List, Optional
from mcp.server.fastmcp.exceptions import ValidationError, ToolError, ResourceError
from agile_team.shared.data_types import FileToFilePromptRequest
from agile_team.shared.validator import validate_and_correct_models
from agile_team.shared.model_router import prompt_model
from agile_team.shared.utils import read_file, write_file, validate_directory_exists
from agile_team.tools.prompt_from_file_to_file import prompt_from_file_to_file

# Default decision maker model
DEFAULT_DECISION_MAKER_MODEL = "openai:o4-mini"

# Default team member models
DEFAULT_TEAM_MODELS = ["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"]

# Default decision prompt template
DEFAULT_DECISION_PROMPT = """
<purpose>
    You are the decision maker of the agile team. You are given a list of responses from your team members. Your job is to take in the original question prompt, and each of the team members' responses, and choose the best direction for the team.
</purpose>
<instructions>
    <instruction>Each team member has proposed an answer to the question posed in the prompt.</instruction>
    <instruction>Given the original question prompt, and each of the team members' responses, choose the best answer.</instruction>
    <instruction>Tally the votes of the team members, choose the best direction, and explain why you chose it.</instruction>
    <instruction>To preserve anonymity, we will use model names instead of real names of your team members. When responding, use the model names in your response.</instruction>
    <instruction>As a decision maker, you breakdown the decision into several categories including: risk, reward, timeline, and resources. In addition to these guiding categories, you also consider the team members' expertise and experience. As a bleeding edge decision maker, you also invent new dimensions of decision making to help you make the best decision for your company.</instruction>
    <instruction>Your final decision maker response should be in markdown format with a comprehensive explanation of your decision. Start the top of the file with a title that says "Team Decision", include a table of contents, briefly describe the question/problem at hand then dive into several sections. One of your first sections should be a quick summary of your decision, then breakdown each of the team members' decisions into sections with your commentary on each. Where we lead into your decision with the categories of your decision making process, and then we lead into your final decision.</instruction>
</instructions>

<original-question>{original_prompt}</original-question>

<team-decisions>
{team_responses}
</team-decisions>
"""


def decision_maker(
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_prompt: str = DEFAULT_DECISION_PROMPT
) -> str:
    """
    Generate responses from multiple LLM models and then use a decision maker model to choose the best direction.
    
    Args:
        from_file: Path to the file containing the prompt
        models_prefixed_by_provider: List of models in the format "provider:model" (if None, defaults to ["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"])
        output_dir: Directory where response files should be saved (defaults to input file's directory/responses)
        output_extension: File extension for output files (e.g., '.py', '.txt', '.md')
        output_path: Optional full output path with filename for the decision document
        decision_maker_model: Model to use for making the decision
        decision_prompt: Custom decision prompt template (if None, uses the default)
        
    Returns:
        Path to the decision output file
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
            team_responses_text += f"""<team-response>
    <model-name>{model_info}</model-name>
    <response>{response}</response>
</team-response>
"""
        except Exception as e:
            # Skip files that can't be read
            continue
    
    # Prepare the decision prompt with the original prompt and team responses
    final_decision_prompt = decision_prompt.format(
        original_prompt=original_prompt,
        team_responses=team_responses_text
    )
    
    # Validate and correct the decision maker model
    validated_models = validate_and_correct_models([decision_maker_model])
    if not validated_models:
        raise ValidationError(f"Invalid decision maker model: {decision_maker_model}")
    
    # Extract the provider and model
    provider, model = validated_models[0]
    
    try:
        # Get decision from the decision maker model
        decision = prompt_model(provider, model, final_decision_prompt)
        
        # Handle the decision output path
        if output_path:
            # Use the exact path specified
            decision_file_path = output_path
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
            
            # Create the decision output filename
            output_filename = f"{file_name}_decision{extension}"
            decision_file_path = os.path.join(team_output_dir, output_filename)
        
        # Write the decision to the output file
        write_file(decision_file_path, decision)
        
        return decision_file_path
        
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
            error_file_path = os.path.join(team_output_dir, f"{file_name}_decision_error{extension}")
        
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(error_file_path) or ".", exist_ok=True)
        
        # Write error to file
        write_file(error_file_path, error_message)
        raise ToolError(error_message)