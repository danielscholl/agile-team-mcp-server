"""
Tests for model router.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
import importlib
from agile_team.shared.model_router import ModelRouter, prompt_model, list_models, list_providers, _get_provider_module
from agile_team.shared.data_types import ModelProviders


@patch('importlib.import_module')
def test_get_provider_module(mock_import_module):
    """Test _get_provider_module method."""
    # Set up mock
    mock_module = MagicMock()
    mock_import_module.return_value = mock_module
    
    # Test getting a provider module
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        result = ModelRouter._get_provider_module("openai")
        assert result == mock_module
        mock_import_module.assert_called_with("agile_team.shared.llm_providers.openai")
    
    # Test using short name
    mock_import_module.reset_mock()
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        result = ModelRouter._get_provider_module("o")
        assert result == mock_module
        mock_import_module.assert_called_with("agile_team.shared.llm_providers.openai")
    
    # Test testing provider (doesn't need API key)
    mock_import_module.reset_mock()
    result = ModelRouter._get_provider_module("testing")
    assert result == mock_module
    mock_import_module.assert_called_with("agile_team.shared.llm_providers.testing")
    
    # Test invalid provider
    with pytest.raises(Exception):
        ModelRouter._get_provider_module("unknown")


@patch('importlib.import_module')
def test_prompt_model(mock_import_module):
    """Test prompt_model method."""
    # Set up mock
    mock_module = MagicMock()
    mock_module.prompt.return_value = "Paris is the capital of France."
    mock_import_module.return_value = mock_module
    
    # Test with full provider name
    response = ModelRouter.prompt_model("openai", "gpt-4o-mini", "What is the capital of France?")
    assert response == "Paris is the capital of France."
    mock_import_module.assert_called_with("agile_team.shared.llm_providers.openai")
    mock_module.prompt.assert_called_with(text="What is the capital of France?", model="gpt-4o-mini")
    
    # Reset mocks for next test
    mock_import_module.reset_mock()
    mock_module.prompt.reset_mock()
    
    # Test with short provider name
    response = ModelRouter.prompt_model("o", "gpt-4o-mini", "What is the capital of France?")
    assert response == "Paris is the capital of France."
    mock_import_module.assert_called_with("agile_team.shared.llm_providers.openai")
    
    # Test with error
    mock_module.prompt.side_effect = ValueError("Test error")
    with pytest.raises(Exception):
        ModelRouter.prompt_model("openai", "gpt-4o-mini", "What is the capital of France?")


def test_prompt_model_with_testing_provider():
    """Test prompt_model method with the testing provider."""
    # Set the TEST_MODE environment variable to enable the testing provider
    with patch.dict(os.environ, {"TEST_MODE": "1"}):
        # No mocking needed, the testing provider will respond with a predictable pattern
        response = ModelRouter.prompt_model("testing", "test-model", "What is the capital of France?")
        assert response == "Paris is the capital of France."
        
        response = ModelRouter.prompt_model("t", "test-model", "What is the largest planet?")
        assert response == "Jupiter is the largest planet in our solar system."
        
        # Test error case
        with pytest.raises(Exception):
            ModelRouter.prompt_model("testing", "test-model", "test error")


@patch('importlib.import_module')
def test_list_models(mock_import_module):
    """Test list_models method."""
    # Set up mock
    mock_module = MagicMock()
    mock_module.list_models.return_value = ["model1", "model2"]
    mock_import_module.return_value = mock_module
    
    # Test with full provider name
    models = ModelRouter.list_models("openai")
    assert models == ["model1", "model2"]
    mock_import_module.assert_called_with("agile_team.shared.llm_providers.openai")
    mock_module.list_models.assert_called_once()
    
    # Reset mocks for next test
    mock_import_module.reset_mock()
    mock_module.list_models.reset_mock()
    
    # Test with short provider name
    models = ModelRouter.list_models("o")
    assert models == ["model1", "model2"]
    
    # Test with testing provider
    mock_import_module.reset_mock()
    mock_module.list_models.reset_mock()
    with patch.dict(os.environ, {"TEST_MODE": "1"}):
        models = ModelRouter.list_models("testing")
        assert models == ["model1", "model2"]
        mock_import_module.assert_called_with("agile_team.shared.llm_providers.testing")
    
    # Test invalid provider
    mock_import_module.side_effect = ValueError("Unknown provider")
    with pytest.raises(Exception):
        ModelRouter.list_models("unknown")


def test_list_models_with_testing_provider():
    """Test list_models method with the testing provider."""
    # Set the TEST_MODE environment variable to enable the testing provider
    with patch.dict(os.environ, {"TEST_MODE": "1"}):
        # No mocking needed, the testing provider will respond with a predictable list
        models = ModelRouter.list_models("testing")
        assert models == ["test-model-1", "test-model-2", "test-model-3"]
        
        models = ModelRouter.list_models("t")
        assert models == ["test-model-1", "test-model-2", "test-model-3"]


def test_list_providers():
    """Test list_providers method."""
    # Test without detailed flag - excluding testing provider in production
    providers = ModelRouter.list_providers()
    assert isinstance(providers, list)
    assert "openai" in providers
    assert "anthropic" in providers
    assert "gemini" in providers
    assert "o" in providers
    assert "a" in providers
    assert "testing" not in providers  # Should not be included in production
    assert "t" not in providers  # Should not be included in production
    
    # Test with testing provider in test mode
    with patch.dict(os.environ, {"TEST_MODE": "1"}):
        providers = ModelRouter.list_providers()
        assert "testing" in providers
        assert "t" in providers
    
    # Test with detailed flag
    providers_detailed = ModelRouter.list_providers(detailed=True)
    assert isinstance(providers_detailed, dict)
    assert "openai" in providers_detailed
    assert "anthropic" in providers_detailed
    assert "o" in providers_detailed["openai"]
    assert "a" in providers_detailed["anthropic"]


def test_backwards_compatibility():
    """Test backwards compatibility functions."""
    with patch('agile_team.shared.model_router.ModelRouter._get_provider_module') as mock_method:
        _get_provider_module("openai")
        mock_method.assert_called_once_with("openai")
    
    with patch('agile_team.shared.model_router.ModelRouter.prompt_model') as mock_method:
        prompt_model("openai", "gpt-4o-mini", "test")
        mock_method.assert_called_once_with("openai", "gpt-4o-mini", "test")
    
    with patch('agile_team.shared.model_router.ModelRouter.list_providers') as mock_method:
        # Check the actual call trace rather than using assert_called_once_with
        list_providers(detailed=True)
        assert mock_method.call_count == 1
        # Get the actual call arguments
        args, kwargs = mock_method.call_args
        assert kwargs.get('detailed') is True or (not kwargs and args and args[0] is True)
    
    with patch('agile_team.shared.model_router.ModelRouter.list_models') as mock_method:
        list_models("openai")
        mock_method.assert_called_once_with("openai")