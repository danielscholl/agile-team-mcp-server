"""
Tests for Ollama provider.
"""

import pytest
import os
from dotenv import load_dotenv
from agile_team.shared.llm_providers import ollama

# Load environment variables
load_dotenv()


def test_list_models():
    """Test listing Ollama models."""
    models = ollama.list_models()
    assert isinstance(models, list)
    assert isinstance(models[0], str)
    assert len(models) > 0


def test_prompt():
    """Test sending prompt to Ollama."""
    # Using llama3 as default model - adjust if needed based on your environment

    # Use the specific model that's available
    try:
        response = ollama.prompt("What is the capital of France?", "llama3.2:1b")
    except ValueError as e:
        # Skip the test if the model isn't available
        pytest.skip(f"Cannot test with llama3.2:1b: {str(e)}")

    # Assertions
    assert isinstance(response, str)
    assert len(response) > 0
    assert "paris" in response.lower() or "Paris" in response
