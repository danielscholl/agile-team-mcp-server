"""Tests for the persona_dm tool."""

import os
import pytest
from unittest.mock import patch, MagicMock
from agile_team.tools.persona_dm import persona_dm
from mcp.server.fastmcp.exceptions import ValidationError, ToolError, ResourceError


@patch('agile_team.tools.persona_dm.os.makedirs')
@patch('agile_team.tools.persona_dm.validate_directory_exists')
@patch('agile_team.tools.persona_dm.prompt_from_file_to_file')
@patch('agile_team.tools.persona_dm.read_file')
@patch('agile_team.tools.persona_dm.validate_and_correct_models')
@patch('agile_team.tools.persona_dm.prompt_model')
@patch('agile_team.tools.persona_dm.write_file')
def test_persona_dm_success(
    mock_write_file, 
    mock_prompt_model, 
    mock_validate_models, 
    mock_read_file, 
    mock_prompt_from_file,
    mock_validate_dir,
    mock_makedirs
):
    """Test successful execution of the persona_dm tool."""
    # Set up mocks
    mock_prompt_from_file.return_value = [
        "/test/responses/test_openai_o4.txt",
        "/test/responses/test_anthropic_claude.txt"
    ]
    mock_read_file.side_effect = [
        "What is the best approach for implementing feature X?",  # Original prompt
        "Implement it with approach A",  # First model response
        "Implement it with approach B"   # Second model response
    ]
    mock_validate_models.return_value = [("openai", "o3")]
    mock_prompt_model.return_value = "Decision: Approach B is better"
    mock_validate_dir.return_value = None  # Mock the directory validation
    mock_makedirs.return_value = None  # Mock directory creation
    
    # Call the function
    result = persona_dm(
        from_file="/test/prompt.txt",
        models_prefixed_by_provider=["openai:o4", "anthropic:claude"],
        persona_dm_model="openai:o3"
    )
    
    # Assert the result
    expected_path = "/test/responses/prompt_persona.md"
    assert result == expected_path
    
    # Validate calls
    mock_prompt_from_file.assert_called_once()
    assert mock_prompt_from_file.call_args[1]['file_path'] == "/test/prompt.txt"
    assert mock_prompt_from_file.call_args[1]['models_prefixed_by_provider'] == ["openai:o4", "anthropic:claude"]
    assert mock_prompt_from_file.call_args[1]['output_dir'] == "/test/responses"
    
    assert mock_read_file.call_count == 3
    
    mock_validate_models.assert_called_once_with(["openai:o3"])
    
    mock_prompt_model.assert_called_once()
    
    mock_write_file.assert_called_once()
    assert mock_write_file.call_args[0][0] == expected_path
    assert mock_write_file.call_args[0][1] == "Decision: Approach B is better"


@patch('agile_team.tools.persona_dm.validate_directory_exists')
def test_persona_dm_validation_error(mock_validate_dir):
    """Test validation error when insufficient models are provided."""
    # Test with no models
    with pytest.raises(ValidationError):
        persona_dm(from_file="test.txt", models_prefixed_by_provider=[])
    
    # Test with only one model
    with pytest.raises(ValidationError):
        persona_dm(from_file="test.txt", models_prefixed_by_provider=["openai:o4"])


@patch('agile_team.tools.persona_dm.os.makedirs')
@patch('agile_team.tools.persona_dm.validate_directory_exists')
@patch('agile_team.tools.persona_dm.prompt_from_file_to_file')
@patch('agile_team.tools.persona_dm.read_file')
@patch('agile_team.tools.persona_dm.validate_and_correct_models')
def test_persona_dm_invalid_model(
    mock_validate_models, 
    mock_read_file, 
    mock_prompt_from_file,
    mock_validate_dir,
    mock_makedirs
):
    """Test error handling when an invalid persona model is provided."""
    # Set up mocks
    mock_prompt_from_file.return_value = [
        "/test/responses/test_openai_o4.txt",
        "/test/responses/test_anthropic_claude.txt"
    ]
    mock_read_file.return_value = "Test prompt"
    mock_validate_models.return_value = []  # No valid models found
    mock_validate_dir.return_value = None  # Mock the directory validation
    mock_makedirs.return_value = None  # Mock directory creation
    
    # Test with invalid persona model
    with pytest.raises(ValidationError):
        persona_dm(
            from_file="/test/prompt.txt",
            models_prefixed_by_provider=["openai:o4", "anthropic:claude"],
            persona_dm_model="invalid:model"
        )


@patch('agile_team.tools.persona_dm.os.makedirs')
@patch('agile_team.tools.persona_dm.validate_directory_exists')
@patch('agile_team.tools.persona_dm.prompt_from_file_to_file')
@patch('agile_team.tools.persona_dm.read_file')
@patch('agile_team.tools.persona_dm.validate_and_correct_models')
@patch('agile_team.tools.persona_dm.prompt_model')
@patch('agile_team.tools.persona_dm.write_file')
def test_persona_dm_prompt_error(
    mock_write_file, 
    mock_prompt_model, 
    mock_validate_models, 
    mock_read_file, 
    mock_prompt_from_file,
    mock_validate_dir,
    mock_makedirs
):
    """Test error handling when the persona model fails."""
    # Set up mocks
    mock_prompt_from_file.return_value = [
        "/test/responses/test_openai_o4.txt",
        "/test/responses/test_anthropic_claude.txt"
    ]
    mock_read_file.side_effect = [
        "Test prompt",  # Original prompt
        "Response 1",   # First model response
        "Response 2"    # Second model response
    ]
    mock_validate_models.return_value = [("openai", "o3")]
    mock_prompt_model.side_effect = Exception("API error")
    mock_validate_dir.return_value = None  # Mock the directory validation
    mock_makedirs.return_value = None  # Mock directory creation
    
    # Test with error from the persona model
    with pytest.raises(ToolError):
        persona_dm(
            from_file="/test/prompt.txt",
            models_prefixed_by_provider=["openai:o4", "anthropic:claude"],
            persona_dm_model="openai:o3"
        )
    
    # Should write an error file
    mock_write_file.assert_called_once()
    assert "_persona_error" in mock_write_file.call_args[0][0]


@patch('agile_team.tools.persona_dm.os.makedirs')
@patch('agile_team.tools.persona_dm.validate_directory_exists')
@patch('agile_team.tools.persona_dm.prompt_from_file_to_file')
@patch('agile_team.tools.persona_dm.read_file')
@patch('agile_team.tools.persona_dm.validate_and_correct_models')
@patch('agile_team.tools.persona_dm.prompt_model')
@patch('agile_team.tools.persona_dm.write_file')
def test_persona_dm_with_custom_output_path(
    mock_write_file, 
    mock_prompt_model, 
    mock_validate_models, 
    mock_read_file, 
    mock_prompt_from_file,
    mock_validate_dir,
    mock_makedirs
):
    """Test persona_dm with custom output path."""
    # Set up mocks
    mock_prompt_from_file.return_value = [
        "/output/test_openai_o4.txt",
        "/output/test_anthropic_claude.txt"
    ]
    mock_read_file.side_effect = [
        "What is the best approach for implementing feature X?",  # Original prompt
        "Implement it with approach A",  # First model response
        "Implement it with approach B"   # Second model response
    ]
    mock_validate_models.return_value = [("openai", "o3")]
    mock_prompt_model.return_value = "Decision: Approach B is better"
    mock_validate_dir.return_value = None  # Mock the directory validation
    mock_makedirs.return_value = None  # Mock directory creation
    
    # Call the function with output_path
    custom_output_path = "/custom/path/final_decision.md"
    result = persona_dm(
        from_file="/test/prompt.txt",
        models_prefixed_by_provider=["openai:o4", "anthropic:claude"],
        persona_dm_model="openai:o3",
        output_path=custom_output_path
    )
    
    # Assert the result
    assert result == custom_output_path
    
    # Validate write_file was called with the custom path
    mock_write_file.assert_called_once_with(
        custom_output_path,
        "Decision: Approach B is better"
    )