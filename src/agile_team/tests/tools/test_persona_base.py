"""Tests for the base persona implementation."""

import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock

from agile_team.tools.persona_base import persona_base, _run_with_single_model, _run_with_decision_maker
from agile_team.shared.config import DEFAULT_MODEL, DEFAULT_TEAM_MODELS, DEFAULT_DECISION_MAKER_MODEL


class TestPersonaBase:
    """Tests for the persona_base functionality."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.test_prompt = "<purpose>Test purpose</purpose>\n<test-request>{analyst_request}</test-request>"
        self.test_content = "Test content for analysis"
        
        # Create a temporary file with test content
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_file.write(self.test_content)
        self.temp_file.close()
    
    def teardown_method(self):
        """Teardown for each test method."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    @patch('agile_team.tools.persona_base.prompt_model')
    @patch('agile_team.tools.persona_base.write_file')
    def test_single_model_workflow(self, mock_write_file, mock_prompt_model):
        """Test the single model workflow."""
        # Setup
        mock_prompt_model.return_value = "Model response"
        mock_write_file.return_value = None
        
        # Create a temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Execute
            result = persona_base(
                persona_name="test_persona",
                persona_prompt=self.test_prompt,
                from_file=self.temp_file.name,
                output_dir=temp_dir
            )
            
            # Verify
            assert result is not None
            assert temp_dir in result
            assert "test_persona" in result
            mock_prompt_model.assert_called_once()
            expected_prompt = self.test_prompt.format(analyst_request=self.test_content)
            assert mock_prompt_model.call_args[0][2] == expected_prompt
            mock_write_file.assert_called_once()
    
    @patch('agile_team.tools.persona_base.persona_dm')
    def test_decision_maker_workflow(self, mock_persona_dm):
        """Test the decision maker workflow."""
        # Setup
        expected_output = "/path/to/result.md"
        mock_persona_dm.return_value = expected_output
        
        # Execute
        with tempfile.TemporaryDirectory() as temp_dir:
            result = persona_base(
                persona_name="test_persona",
                persona_prompt=self.test_prompt,
                from_file=self.temp_file.name,
                output_dir=temp_dir,
                use_decision_maker=True
            )
            
            # Verify
            assert result == expected_output
            mock_persona_dm.assert_called_once()
            # Verify the temporary file being created and passed to persona_dm
            temp_file_path = mock_persona_dm.call_args[1]['from_file']
            assert os.path.exists(temp_file_path) == False  # Should be deleted after use
    
    def test_default_model_handling(self):
        """Test that default models are handled correctly."""
        with patch('agile_team.tools.persona_base._run_with_single_model') as mock_single:
            mock_single.return_value = "result.md"
            
            # Without specifying a model, should use DEFAULT_MODEL
            persona_base(
                persona_name="test",
                persona_prompt="test",
                from_file=self.temp_file.name
            )
            
            # Verify DEFAULT_MODEL was used
            assert mock_single.call_args[1]['models_prefixed_by_provider'] == [DEFAULT_MODEL]
    
    def test_default_decision_maker_models_handling(self):
        """Test that default decision maker models are handled correctly."""
        with patch('agile_team.tools.persona_base._run_with_decision_maker') as mock_dm:
            mock_dm.return_value = "result.md"
            
            # Without specifying decision maker models, should use DEFAULT_TEAM_MODELS
            persona_base(
                persona_name="test",
                persona_prompt="test",
                from_file=self.temp_file.name,
                use_decision_maker=True
            )
            
            # Verify DEFAULT_TEAM_MODELS was passed
            assert mock_dm.call_args[1]['decision_maker_models'] == DEFAULT_TEAM_MODELS