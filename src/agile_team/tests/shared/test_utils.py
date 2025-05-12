"""Tests for utility functions."""

import os
import pytest
from mcp.server.fastmcp.exceptions import ValidationError, ResourceError
from agile_team.shared.utils import (
    parse_provider_model,
    validate_file_exists,
    format_error_response,
    weak_provider_and_model
)


def test_parse_provider_model_valid():
    """Test parsing valid provider:model string."""
    provider, model = parse_provider_model("openai:gpt-4")
    assert provider == "openai"
    assert model == "gpt-4"


def test_parse_provider_model_invalid():
    """Test parsing invalid provider:model string."""
    with pytest.raises(ValidationError):
        parse_provider_model("invalid-format")
    
    with pytest.raises(ValidationError):
        parse_provider_model(":")
        
    with pytest.raises(ValidationError):
        parse_provider_model("provider:")
        
    with pytest.raises(ValidationError):
        parse_provider_model(":model")


def test_validate_file_exists(tmp_path):
    """Test file existence validation."""
    # Create a temporary file
    test_file = tmp_path / "test.txt"
    with open(test_file, "w") as f:
        f.write("test content")
    
    # Should not raise an exception
    validate_file_exists(str(test_file))
    
    # Should raise ResourceError for non-existent file
    non_existent_file = tmp_path / "nonexistent.txt"
    with pytest.raises(ResourceError):
        validate_file_exists(str(non_existent_file))


def test_format_error_response():
    """Test error response formatting."""
    response = format_error_response("TEST_ERROR", "Test error message")
    assert response["error"]["code"] == "TEST_ERROR"
    assert response["error"]["message"] == "Test error message"
    assert "details" not in response["error"]
    
    response = format_error_response(
        "TEST_ERROR", 
        "Test error message", 
        {"detail": "Additional info"}
    )
    assert response["error"]["details"]["detail"] == "Additional info"


def test_weak_provider_and_model():
    """Test weak provider and model correction."""
    # Test provider correction
    provider, model = weak_provider_and_model("oai", "gpt-4", ["gpt-4"])
    assert provider == "openai"
    assert model == "gpt-4"
    
    # Test model correction
    provider, model = weak_provider_and_model("openai", "gpt4", ["gpt-4", "gpt-3.5-turbo"])
    assert provider == "openai"
    assert model == "gpt-4"
    
    # Test default model when not found
    provider, model = weak_provider_and_model("openai", "nonexistent", ["gpt-4", "gpt-3.5-turbo"])
    assert provider == "openai"
    assert model == "gpt-4"