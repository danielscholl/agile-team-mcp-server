"""
Tests for prompt_from_file functionality.
"""

import pytest
import os
import tempfile
from dotenv import load_dotenv
from agile_team.tools.prompt_from_file import prompt_from_file
from mcp.server.fastmcp.exceptions import ResourceError

# Load environment variables
load_dotenv()


def test_nonexistent_file():
    """Test with non-existent file."""
    with pytest.raises(ResourceError):
        prompt_from_file("/non/existent/file.txt", ["openai:gpt-4o-mini"])


def test_file_read():
    """Test that the file is read correctly and processes with real API call."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    # Create temporary file with a simple question
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        temp.write("What is the capital of France?")
        temp_path = temp.name
    
    try:
        # Make real API call
        response = prompt_from_file(temp_path, ["openai:gpt-4o-mini"])
        
        # Assertions
        assert isinstance(response, list)
        assert len(response) == 1
        assert isinstance(response[0], str)
        assert "paris" in response[0].lower() or "Paris" in response[0]
    finally:
        # Clean up
        os.unlink(temp_path)