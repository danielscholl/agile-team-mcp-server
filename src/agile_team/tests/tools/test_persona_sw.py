"""Tests for the Spec Writer persona implementation."""

import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock

from agile_team.tools.persona_sw import persona_sw, DEFAULT_SW_PROMPT_CONTENT, DEFAULT_SW_DECISION_PROMPT
from agile_team.shared.config import DEFAULT_MODEL, DEFAULT_TEAM_MODELS, DEFAULT_DECISION_MAKER_MODEL


class TestPersonaSw:
    """Tests for the Spec Writer persona functionality."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.test_content = "Create a specification for a RESTful API that manages user authentication and authorization."
        
        # Create a temporary file with test content
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_file.write(self.test_content)
        self.temp_file.close()
    
    def teardown_method(self):
        """Teardown for each test method."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    @patch('agile_team.tools.persona_sw.persona_base')
    def test_persona_sw_default_parameters(self, mock_persona_base):
        """Test the Spec Writer persona with default parameters."""
        # Setup
        expected_output = "/path/to/output.md"
        mock_persona_base.return_value = expected_output
        
        # Execute
        result = persona_sw(from_file=self.temp_file.name)
        
        # Verify
        assert result == expected_output
        mock_persona_base.assert_called_once()
        
        # Check that persona_base was called with the correct parameters
        call_kwargs = mock_persona_base.call_args[1]
        assert call_kwargs['persona_name'] == "spec_writer"
        assert call_kwargs['persona_prompt'] == DEFAULT_SW_PROMPT_CONTENT
        assert call_kwargs['from_file'] == self.temp_file.name
        assert call_kwargs['use_decision_maker'] == False
        assert call_kwargs['decision_maker_model'] == DEFAULT_DECISION_MAKER_MODEL
    
    @patch('agile_team.tools.persona_sw.persona_base')
    def test_persona_sw_with_decision_maker(self, mock_persona_base):
        """Test the Spec Writer persona with decision maker enabled."""
        # Setup
        expected_output = "/path/to/decision.md"
        mock_persona_base.return_value = expected_output
        
        # Execute
        result = persona_sw(
            from_file=self.temp_file.name,
            use_decision_maker=True,
            decision_maker_models=["openai:model1", "anthropic:model2"]
        )
        
        # Verify
        assert result == expected_output
        mock_persona_base.assert_called_once()
        
        # Check that persona_base was called with the correct parameters
        call_kwargs = mock_persona_base.call_args[1]
        assert call_kwargs['persona_name'] == "spec_writer"
        assert call_kwargs['use_decision_maker'] == True
        assert call_kwargs['decision_maker_models'] == ["openai:model1", "anthropic:model2"]
    
    @patch('agile_team.tools.persona_sw.persona_base')
    def test_persona_sw_custom_prompt(self, mock_persona_base):
        """Test the Spec Writer persona with a custom prompt."""
        # Setup
        expected_output = "/path/to/output.md"
        mock_persona_base.return_value = expected_output
        custom_prompt = "<custom>Test prompt {request_data}</custom>"
        
        # Execute
        result = persona_sw(
            from_file=self.temp_file.name,
            sw_prompt=custom_prompt
        )
        
        # Verify
        assert result == expected_output
        mock_persona_base.assert_called_once()
        
        # Check that persona_base was called with the correct parameters
        call_kwargs = mock_persona_base.call_args[1]
        assert call_kwargs['persona_prompt'] == custom_prompt
    
    @patch('agile_team.tools.persona_sw.persona_base')
    def test_persona_sw_output_path_handling(self, mock_persona_base):
        """Test the Spec Writer persona with custom output path."""
        # Setup
        expected_output = "/custom/path/output.md"
        mock_persona_base.return_value = expected_output
        
        # Execute
        result = persona_sw(
            from_file=self.temp_file.name,
            output_path=expected_output
        )
        
        # Verify
        assert result == expected_output
        mock_persona_base.assert_called_once()
        
        # Check that persona_base was called with the correct parameters
        call_kwargs = mock_persona_base.call_args[1]
        assert call_kwargs['output_path'] == expected_output
    
    @patch('agile_team.tools.persona_sw.persona_base')
    def test_persona_sw_custom_decision_maker_prompt(self, mock_persona_base):
        """Test the Spec Writer persona with custom decision maker prompt."""
        # Setup
        expected_output = "/path/to/decision.md"
        mock_persona_base.return_value = expected_output
        custom_decision_prompt = "<custom>Decision maker prompt {team_responses}</custom>"
        
        # Execute
        result = persona_sw(
            from_file=self.temp_file.name,
            use_decision_maker=True,
            decision_maker_prompt=custom_decision_prompt
        )
        
        # Verify
        assert result == expected_output
        mock_persona_base.assert_called_once()
        
        # Check that persona_base was called with the correct parameters
        call_kwargs = mock_persona_base.call_args[1]
        assert call_kwargs['decision_maker_prompt'] == custom_decision_prompt