"""Tests for the decision maker tool."""

import os
import pytest
from unittest.mock import patch, MagicMock
from agile_team.tools.decision_maker import decision_maker
from mcp.server.fastmcp.exceptions import ValidationError, ToolError, ResourceError


@patch('agile_team.tools.decision_maker.validate_directory_exists')
@patch('agile_team.tools.decision_maker.prompt_from_file_to_file')
@patch('agile_team.tools.decision_maker.read_file')
@patch('agile_team.tools.decision_maker.validate_and_correct_models')
@patch('agile_team.tools.decision_maker.prompt_model')
@patch('agile_team.tools.decision_maker.write_file')
def test_decision_maker_success(
    mock_write_file, 
    mock_prompt_model, 
    mock_validate_models, 
    mock_read_file, 
    mock_prompt_from_file,
    mock_validate_dir
):
    """Test successful execution of the decision maker tool."""
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
    
    # Call the function
    result = decision_maker(
        from_file="/test/prompt.txt",
        output_dir="/output",
        models_prefixed_by_provider=["openai:o4", "anthropic:claude"],
        decision_maker_model="openai:o3"
    )
    
    # Assert the result
    assert result == "/output/decision_maker_decision.md"
    
    # Validate calls
    mock_prompt_from_file.assert_called_once_with(
        file_path="/test/prompt.txt",
        models_prefixed_by_provider=["openai:o4", "anthropic:claude"],
        output_dir="/output"
    )
    
    assert mock_read_file.call_count == 3
    
    mock_validate_models.assert_called_once_with(["openai:o3"])
    
    mock_prompt_model.assert_called_once()
    
    mock_write_file.assert_called_once_with(
        "/output/decision_maker_decision.md",
        "Decision: Approach B is better"
    )


@patch('agile_team.tools.decision_maker.validate_directory_exists')
def test_decision_maker_validation_error(mock_validate_dir):
    """Test validation error when insufficient models are provided."""
    # Test with no models
    with pytest.raises(ValidationError):
        decision_maker(from_file="test.txt", models_prefixed_by_provider=[])
    
    # Test with only one model
    with pytest.raises(ValidationError):
        decision_maker(from_file="test.txt", models_prefixed_by_provider=["openai:o4"])


@patch('agile_team.tools.decision_maker.validate_directory_exists')
@patch('agile_team.tools.decision_maker.prompt_from_file_to_file')
@patch('agile_team.tools.decision_maker.read_file')
@patch('agile_team.tools.decision_maker.validate_and_correct_models')
def test_decision_maker_invalid_model(
    mock_validate_models, 
    mock_read_file, 
    mock_prompt_from_file,
    mock_validate_dir
):
    """Test error handling when an invalid decision maker model is provided."""
    # Set up mocks
    mock_prompt_from_file.return_value = [
        "/output/test_openai_o4.txt",
        "/output/test_anthropic_claude.txt"
    ]
    mock_read_file.return_value = "Test prompt"
    mock_validate_models.return_value = []  # No valid models found
    mock_validate_dir.return_value = None  # Mock the directory validation
    
    # Test with invalid decision maker model
    with pytest.raises(ValidationError):
        decision_maker(
            from_file="/test/prompt.txt",
            output_dir="/output",
            models_prefixed_by_provider=["openai:o4", "anthropic:claude"],
            decision_maker_model="invalid:model"
        )


@patch('agile_team.tools.decision_maker.validate_directory_exists')
@patch('agile_team.tools.decision_maker.prompt_from_file_to_file')
@patch('agile_team.tools.decision_maker.read_file')
@patch('agile_team.tools.decision_maker.validate_and_correct_models')
@patch('agile_team.tools.decision_maker.prompt_model')
@patch('agile_team.tools.decision_maker.write_file')
def test_decision_maker_prompt_error(
    mock_write_file, 
    mock_prompt_model, 
    mock_validate_models, 
    mock_read_file, 
    mock_prompt_from_file,
    mock_validate_dir
):
    """Test error handling when the decision maker model fails."""
    # Set up mocks
    mock_prompt_from_file.return_value = [
        "/output/test_openai_o4.txt",
        "/output/test_anthropic_claude.txt"
    ]
    mock_read_file.side_effect = [
        "Test prompt",  # Original prompt
        "Response 1",   # First model response
        "Response 2"    # Second model response
    ]
    mock_validate_models.return_value = [("openai", "o3")]
    mock_prompt_model.side_effect = Exception("API error")
    mock_validate_dir.return_value = None  # Mock the directory validation
    
    # Test with error from the decision maker model
    with pytest.raises(ToolError):
        decision_maker(
            from_file="/test/prompt.txt",
            output_dir="/output",
            models_prefixed_by_provider=["openai:o4", "anthropic:claude"],
            decision_maker_model="openai:o3"
        )
    
    # Should write an error file
    mock_write_file.assert_called_once()
    assert "decision_maker_error.md" in mock_write_file.call_args[0][0]