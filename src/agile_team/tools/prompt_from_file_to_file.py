"""Prompt from file to file tool implementation."""

import os
from typing import List
from mcp.server.fastmcp.exceptions import ValidationError, ToolError, ResourceError
from agile_team.shared.data_types import FileToFilePromptRequest
from agile_team.shared.validator import validate_and_correct_models
from agile_team.shared.model_router import prompt_model
from agile_team.shared.utils import read_file, write_file, validate_directory_exists


def prompt_from_file_to_file(
    file: str, 
    models_prefixed_by_provider: List[str], 
    output_dir: str = "."
) -> List[str]:
    """
    Read a prompt from a file, send it to multiple models, and write responses to files.
    
    Args:
        file: Path to the file containing the prompt
        models_prefixed_by_provider: List of models in the format "provider:model"
        output_dir: Directory where response files should be saved
        
    Returns:
        List of paths to the output files
    """
    # Validate request
    request = FileToFilePromptRequest(
        file=file, 
        models_prefixed_by_provider=models_prefixed_by_provider,
        output_dir=output_dir
    )
    
    # Read prompt from file
    try:
        prompt_text = read_file(request.file)
    except ResourceError as e:
        raise ResourceError(f"Failed to read prompt file: {str(e)}")
    
    # Validate and correct models
    validated_models = validate_and_correct_models(request.models_prefixed_by_provider)
    
    # Validate output directory
    try:
        validate_directory_exists(request.output_dir)
    except ResourceError as e:
        raise ResourceError(f"Invalid output directory: {str(e)}")
    
    # Get base filename from input file
    base_filename = os.path.basename(request.file)
    file_name, _ = os.path.splitext(base_filename)
    
    # Send prompt to each model and write responses to files
    output_files = []
    for provider, model in validated_models:
        try:
            # Generate a safe filename from provider and model
            safe_model = model.replace("/", "_").replace(":", "_")
            output_filename = f"{file_name}_{provider}_{safe_model}.txt"
            output_path = os.path.join(request.output_dir, output_filename)
            
            # Get model response
            response = prompt_model(provider, model, prompt_text)
            
            # Write response to file
            write_file(output_path, response)
            
            output_files.append(output_path)
        except Exception as e:
            # If there's an error, create an error file
            error_filename = f"{file_name}_{provider}_{model}_error.txt"
            error_path = os.path.join(request.output_dir, error_filename)
            write_file(error_path, f"Error from {provider}:{model}: {str(e)}")
            output_files.append(error_path)
    
    return output_files