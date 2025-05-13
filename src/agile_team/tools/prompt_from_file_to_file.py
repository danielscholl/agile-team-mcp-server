"""Prompt from file to file tool implementation."""

import os
from typing import List
from mcp.server.fastmcp.exceptions import ValidationError, ToolError, ResourceError
from agile_team.shared.data_types import FileToFilePromptRequest
from agile_team.shared.validator import validate_and_correct_models
from agile_team.shared.model_router import prompt_model
from agile_team.shared.utils import read_file, write_file, validate_directory_exists


def prompt_from_file_to_file(
    file_path: str, 
    models_prefixed_by_provider: List[str], 
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None
) -> List[str]:
    """
    Read a prompt from a file, send it to multiple models, and write responses to files.
    
    Args:
        file_path: Path to the file containing the prompt
        models_prefixed_by_provider: List of models in the format "provider:model"
        output_dir: Directory where response files should be saved (defaults to input file's directory)
        output_extension: File extension for output files (e.g., '.py', '.txt', '.md')
                         If None, defaults to '.txt'
        output_path: Optional full output path with filename. If provided, the extension
                     from this path will be used (overrides output_extension).
        
    Returns:
        List of paths to the output files
    """
    # Handle case with output_path provided but no output_dir
    if output_path and output_dir is None:
        # Extract the directory from output_path to use as output_dir
        output_dir = os.path.dirname(output_path) or "."
    # Handle case with no output_dir specified (use input file's directory)
    elif output_dir is None:
        output_dir = os.path.dirname(file_path) or "."
        
    # Validate request
    request = FileToFilePromptRequest(
        file_path=file_path, 
        models_prefixed_by_provider=models_prefixed_by_provider,
        output_dir=output_dir,
        output_extension=output_extension,
        output_path=output_path
    )
    
    # Read prompt from file
    try:
        prompt_text = read_file(request.file_path)
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
    base_filename = os.path.basename(request.file_path)
    file_name, _ = os.path.splitext(base_filename)
    
    # Determine file extension to use
    extension = ".txt"  # Default extension
    
    if request.output_path:
        # Extract extension from output_path if provided
        _, output_ext = os.path.splitext(request.output_path)
        if output_ext:
            extension = output_ext
    elif request.output_extension:
        # Use provided output_extension
        extension = request.output_extension
    
    # Make sure the extension starts with a dot
    if not extension.startswith("."):
        extension = f".{extension}"
        
    # Cache the output extension for reuse
    normalized_extension = extension
    
    # Send prompt to each model and write responses to files
    output_files = []
    
    # Determine if we should use the exact output path
    exact_path_requested = request.output_path is not None
    single_model_requested = len(validated_models) == 1
    
    for idx, (provider, model) in enumerate(validated_models):
        try:
            # Determine output file path
            if exact_path_requested and single_model_requested:
                # Case 1: Output path specified and only one model - use exact path
                file_path = request.output_path
            elif exact_path_requested and not single_model_requested:
                # Case 2: Output path specified but multiple models - use directory 
                # from output_path but add model names to filename
                output_dir = os.path.dirname(request.output_path) or "."
                basename = os.path.basename(request.output_path)
                name_part, _ = os.path.splitext(basename)
                safe_model = model.replace("/", "_").replace(":", "_")
                output_filename = f"{name_part}_{provider}_{safe_model}{normalized_extension}"
                file_path = os.path.join(output_dir, output_filename)
            else:
                # Case 3: Standard naming with output_dir + provider + model + extension
                safe_model = model.replace("/", "_").replace(":", "_")
                output_filename = f"{file_name}_{provider}_{safe_model}{normalized_extension}"
                file_path = os.path.join(request.output_dir, output_filename)
            
            # Get model response
            response = prompt_model(provider, model, prompt_text)
            
            # Make sure the output directory exists
            output_directory = os.path.dirname(file_path)
            if output_directory and not os.path.exists(output_directory):
                os.makedirs(output_directory, exist_ok=True)
                
            # Write response to file
            write_file(file_path, response)
            
            output_files.append(file_path)
        except Exception as e:
            if exact_path_requested and single_model_requested:
                # Case 1: Error with exact path - create error file next to the specified output path
                dir_path = os.path.dirname(request.output_path)
                base_name = os.path.basename(request.output_path)
                name, ext = os.path.splitext(base_name)
                error_path = os.path.join(dir_path, f"{name}_error{ext}")
            elif exact_path_requested and not single_model_requested:
                # Case 2: Error with multiple models but output path specified
                output_dir = os.path.dirname(request.output_path) or "."
                basename = os.path.basename(request.output_path)
                name_part, _ = os.path.splitext(basename)
                error_filename = f"{name_part}_{provider}_{model}_error{normalized_extension}"
                error_path = os.path.join(output_dir, error_filename)
            else:
                # Case 3: Standard error filename
                error_filename = f"{file_name}_{provider}_{model}_error{normalized_extension}"
                error_path = os.path.join(request.output_dir, error_filename)
                
            # Create parent directory if needed
            error_dir = os.path.dirname(error_path)
            if error_dir and not os.path.exists(error_dir):
                os.makedirs(error_dir, exist_ok=True)
                
            write_file(error_path, f"Error from {provider}:{model}: {str(e)}")
            output_files.append(error_path)
    
    return output_files