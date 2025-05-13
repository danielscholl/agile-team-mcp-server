"""Base persona implementation for reusable persona functionality."""

import os
import tempfile
from typing import List, Optional
from mcp.server.fastmcp.exceptions import ValidationError, ToolError, ResourceError

from agile_team.shared.config import DEFAULT_MODEL, DEFAULT_TEAM_MODELS, DEFAULT_DECISION_MAKER_MODEL
from agile_team.shared.validator import validate_and_correct_models
from agile_team.shared.model_router import prompt_model
from agile_team.shared.utils import read_file, write_file
from agile_team.tools.persona_dm import persona_dm, DEFAULT_PERSONA_PROMPT


def persona_base(
    persona_name: str,
    persona_prompt: str,
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    use_decision_maker: bool = False,
    decision_maker_models: List[str] = None,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
    """
    Base function for all personas, providing common functionality.
    
    Args:
        persona_name: Name of the persona (e.g., "business_analyst")
        persona_prompt: The prompt template for the persona
        from_file: Path to the file containing the input text
        models_prefixed_by_provider: List of models to use (if None and not using decision maker, uses DEFAULT_MODEL as a single item list)
        output_dir: Directory where response files should be saved
        output_extension: File extension for output files
        output_path: Optional full output path with filename
        use_decision_maker: Whether to use the decision maker functionality
        decision_maker_models: Models to use if use_decision_maker is True (if None, uses DEFAULT_TEAM_MODELS)
        decision_maker_model: Model to use for decision making (defaults to DEFAULT_DECISION_MAKER_MODEL)
        decision_maker_prompt: Custom persona prompt template for decision making
    
    Returns:
        Path to the output file
    """
    # Set default models if none provided
    if models_prefixed_by_provider is None:
        models_prefixed_by_provider = [DEFAULT_MODEL]
        
    # Set default decision maker models if none provided
    if decision_maker_models is None:
        decision_maker_models = DEFAULT_TEAM_MODELS
    
    # Handle path parameters based on input
    if output_path and output_dir is None:
        # Extract directory from output_path
        output_directory = os.path.dirname(output_path) or "."
    elif output_dir is None:
        # Use from_file's directory + responses by default
        input_file_dir = os.path.dirname(from_file) or "."
        output_directory = os.path.join(input_file_dir, "responses")
    else:
        # Use provided output_dir
        output_directory = output_dir
        
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Read the content from the input file
    try:
        input_content = read_file(from_file)
    except ResourceError as e:
        raise ResourceError(f"Failed to read input file: {str(e)}")
    
    # Format the persona prompt with the input content
    formatted_prompt = persona_prompt.format(analyst_request=input_content)
    
    if use_decision_maker:
        # Use the decision maker workflow
        return _run_with_decision_maker(
            persona_name=persona_name,
            formatted_prompt=formatted_prompt,
            from_file=from_file,
            decision_maker_models=decision_maker_models,
            output_directory=output_directory,
            output_extension=output_extension,
            output_path=output_path,
            decision_maker_model=decision_maker_model,
            decision_maker_prompt=decision_maker_prompt
        )
    else:
        # Use the single model workflow
        return _run_with_single_model(
            persona_name=persona_name,
            formatted_prompt=formatted_prompt,
            from_file=from_file,
            models_prefixed_by_provider=models_prefixed_by_provider,
            output_directory=output_directory,
            output_extension=output_extension,
            output_path=output_path
        )


def _run_with_single_model(
    persona_name: str,
    formatted_prompt: str,
    from_file: str,
    models_prefixed_by_provider: List[str],
    output_directory: str,
    output_extension: str,
    output_path: str
) -> str:
    """Run a persona with a single model."""
    # Validate models
    validated_models = validate_and_correct_models(models_prefixed_by_provider)
    if not validated_models:
        raise ValidationError(f"Invalid models: {models_prefixed_by_provider}")
    
    # Extract the provider and model (only use the first one)
    provider, model = validated_models[0]
    
    try:
        # Get response from the model
        response = prompt_model(provider, model, formatted_prompt)
        
        # Handle the output path
        if output_path:
            # Use the exact path specified
            result_file_path = output_path
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        else:
            # Determine the file extension to use (.md by default)
            extension = ".md"
            if output_extension:
                extension = output_extension if output_extension.startswith(".") else f".{output_extension}"
                
            # Extract base name from input file
            base_filename = os.path.basename(from_file)
            file_name, _ = os.path.splitext(base_filename)
            
            # Create the output filename with persona and model info
            model_info = f"{provider}_{model}".replace(":", "_")
            output_filename = f"{file_name}_{persona_name}_{model_info}{extension}"
            result_file_path = os.path.join(output_directory, output_filename)
        
        # Write the response to the output file
        write_file(result_file_path, response)
        
        return result_file_path
        
    except Exception as e:
        # Handle errors when getting a response
        error_message = f"Error getting response from {provider}:{model}: {str(e)}"
        
        # Determine error file path
        if output_path:
            # Create error file next to the specified output path
            dir_path = os.path.dirname(output_path) or "."
            base_name = os.path.basename(output_path)
            name, ext = os.path.splitext(base_name)
            error_file_path = os.path.join(dir_path, f"{name}_error{ext}")
        else:
            # Create standard error file in the output directory
            base_filename = os.path.basename(from_file)
            file_name, _ = os.path.splitext(base_filename)
            extension = ".md"
            if output_extension:
                extension = output_extension if output_extension.startswith(".") else f".{output_extension}"
            error_file_path = os.path.join(output_directory, f"{file_name}_{persona_name}_error{extension}")
        
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(error_file_path) or ".", exist_ok=True)
        
        # Write error to file
        write_file(error_file_path, error_message)
        raise ToolError(error_message)


def _run_with_decision_maker(
    persona_name: str,
    formatted_prompt: str,
    from_file: str,
    decision_maker_models: List[str],
    output_directory: str,
    output_extension: str,
    output_path: str,
    decision_maker_model: str,
    decision_maker_prompt: str
) -> str:
    """Run a persona with the decision maker functionality."""
    try:
        # Create a temporary file with the persona prompt
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(formatted_prompt)
        
        # Run the persona_dm function with the temporary file
        result_path = persona_dm(
            from_file=temp_file_path,
            models_prefixed_by_provider=decision_maker_models,
            output_dir=output_directory,
            output_extension=output_extension,
            output_path=output_path,
            persona_dm_model=decision_maker_model,
            persona_prompt=decision_maker_prompt
        )
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return result_path
        
    except Exception as e:
        # Handle errors with the decision maker process
        error_message = f"Error in decision maker process for {persona_name}: {str(e)}"
        
        # Determine error file path
        if output_path:
            # Create error file next to the specified output path
            dir_path = os.path.dirname(output_path) or "."
            base_name = os.path.basename(output_path)
            name, ext = os.path.splitext(base_name)
            error_file_path = os.path.join(dir_path, f"{name}_error{ext}")
        else:
            # Create standard error file in the output directory
            base_filename = os.path.basename(from_file)
            file_name, _ = os.path.splitext(base_filename)
            extension = ".md"
            if output_extension:
                extension = output_extension if output_extension.startswith(".") else f".{output_extension}"
            error_file_path = os.path.join(output_directory, f"{file_name}_{persona_name}_decision_making_error{extension}")
        
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(error_file_path) or ".", exist_ok=True)
        
        # Write error to file
        write_file(error_file_path, error_message)
        
        # Try to clean up the temporary file if it still exists
        try:
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        except:
            pass
            
        raise ToolError(error_message)