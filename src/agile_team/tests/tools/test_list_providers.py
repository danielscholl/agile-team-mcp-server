"""Tests for the list_providers tool."""

import pytest
from agile_team.tools.list_providers import list_providers


def test_list_providers():
    """Test that list_providers returns expected providers."""
    providers = list_providers()
    
    # Check that the list is not empty
    assert len(providers) > 0
    
    # Check that main providers are included
    assert "openai" in providers
    assert "anthropic" in providers
    assert "google" in providers
    
    # Check that some aliases are included
    assert "oai" in providers or "gpt" in providers  # openai aliases
    assert "claude" in providers  # anthropic alias