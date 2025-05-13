"""
Tests for prompt_from_file_to_file functionality.
"""

import pytest
import os
import tempfile
import shutil
import pathlib
from dotenv import load_dotenv
from agile_team.tools.prompt_from_file_to_file import prompt_from_file_to_file

# Load environment variables
load_dotenv()


def test_directory_creation_and_file_writing():
    """Test that the output directory is created and files are written with real API responses."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    # Create temporary input file with a simple question
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write("What is the capital of France?")
        input_path = temp_file.name
    
    # Create a deep non-existent directory path
    temp_dir = os.path.join(tempfile.gettempdir(), "agile_team_test_dir", "output")
    
    try:
        # Make real API call
        file_paths = prompt_from_file_to_file(
            input_path, 
            ["openai:gpt-4o-mini"],
            temp_dir
        )
        
        # Assertions
        assert isinstance(file_paths, list)
        assert len(file_paths) == 1
        
        # Check that the file exists
        assert os.path.exists(file_paths[0])
        
        # Check that the file has a .txt extension (based on implementation)
        assert file_paths[0].endswith('.txt')
        
        # Check file content contains the expected response
        with open(file_paths[0], 'r') as f:
            content = f.read()
            assert "paris" in content.lower() or "Paris" in content
    finally:
        # Clean up
        os.unlink(input_path)
        # Remove the created directory and all its contents
        if os.path.exists(os.path.dirname(temp_dir)):
            shutil.rmtree(os.path.dirname(temp_dir))


def test_custom_file_extension():
    """Test that the output files use the specified file extension."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    # Create temporary input file with a simple prompt for Python code
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write("Write a Python function to calculate the factorial of a number.")
        input_path = temp_file.name
    
    # Create a temporary directory for output
    temp_dir = os.path.join(tempfile.gettempdir(), "agile_team_test_dir", "py_output")
    
    try:
        # Make real API call with custom extension
        file_paths = prompt_from_file_to_file(
            input_path, 
            ["openai:gpt-4o-mini"],
            temp_dir,
            output_extension="py"
        )
        
        # Assertions
        assert isinstance(file_paths, list)
        assert len(file_paths) == 1
        
        # Check that the file exists
        assert os.path.exists(file_paths[0])
        
        # Check that the file has the requested .py extension
        assert file_paths[0].endswith('.py')
        
        # Check file content contains Python code markers
        with open(file_paths[0], 'r') as f:
            content = f.read()
            assert "def factorial" in content.lower()
    finally:
        # Clean up
        os.unlink(input_path)
        # Remove the created directory and all its contents
        if os.path.exists(os.path.dirname(temp_dir)):
            shutil.rmtree(os.path.dirname(temp_dir))


def test_output_path_extension():
    """Test that the extension is extracted correctly from output_path."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    # Create temporary input file with a simple prompt for Python code
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write("Write a Python function to calculate the factorial of a number.")
        input_path = temp_file.name
    
    # Create a temporary directory for output
    temp_dir = os.path.join(tempfile.gettempdir(), "agile_team_test_dir", "output_path_test")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Specify a full output path with a .py extension
    output_path = os.path.join(temp_dir, "my_factorial_function.py")
    
    try:
        # Make real API call with output_path
        file_paths = prompt_from_file_to_file(
            input_path, 
            ["openai:gpt-4o-mini"],
            temp_dir,
            output_path=output_path
        )
        
        # Assertions
        assert isinstance(file_paths, list)
        assert len(file_paths) == 1
        
        # Check that the file exists
        assert os.path.exists(file_paths[0])
        
        # Check that the file has the .py extension from output_path
        assert file_paths[0].endswith('.py')
        
        # Check file content contains Python code markers
        with open(file_paths[0], 'r') as f:
            content = f.read()
            assert "def factorial" in content.lower()
    finally:
        # Clean up
        os.unlink(input_path)
        # Remove the created directory and all its contents
        if os.path.exists(temp_dir):
            shutil.rmtree(os.path.dirname(temp_dir))


def test_exact_output_path():
    """Test that the exact output path is used when specified."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    # Create temporary input file with a simple prompt for Python code
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write("Write a Python function to calculate the factorial of a number.")
        input_path = temp_file.name
    
    # Create a nested temporary directory structure for output
    temp_output_dir = os.path.join(tempfile.gettempdir(), "agile_team_test_dir", "custom_output", "nested")
    
    # Create a specific output filename that doesn't match the standard naming pattern
    custom_filename = "custom_factorial.py"
    full_output_path = os.path.join(temp_output_dir, custom_filename)
    
    try:
        # Make real API call with exact output path
        file_paths = prompt_from_file_to_file(
            input_path, 
            ["openai:gpt-4o-mini"],
            output_path=full_output_path
        )
        
        # Assertions
        assert isinstance(file_paths, list)
        assert len(file_paths) == 1
        
        # Check that the file exists
        assert os.path.exists(file_paths[0])
        
        # Check that the exact path was used, including directory creation
        assert file_paths[0] == full_output_path
        
        # Check that the file has the correct name
        assert os.path.basename(file_paths[0]) == custom_filename
        
        # Check file content contains Python code markers
        with open(file_paths[0], 'r') as f:
            content = f.read()
            assert "def factorial" in content.lower()
    finally:
        # Clean up
        os.unlink(input_path)
        # Remove the created directory and all its contents
        if os.path.exists(os.path.dirname(os.path.dirname(temp_output_dir))):
            shutil.rmtree(os.path.dirname(os.path.dirname(temp_output_dir)))


def test_default_output_directory():
    """Test that the output directory defaults to input file's directory when not specified."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
    
    # Create a nested temporary directory structure
    temp_base_dir = os.path.join(tempfile.gettempdir(), "agile_team_test_dir", "input_dir")
    os.makedirs(temp_base_dir, exist_ok=True)
    
    # Create input file in the nested directory
    input_path = os.path.join(temp_base_dir, "prompt_file.txt")
    with open(input_path, 'w') as f:
        f.write("What is the capital of Spain?")
    
    try:
        # Make real API call without specifying output_dir
        file_paths = prompt_from_file_to_file(
            input_path, 
            ["openai:gpt-4o-mini"]
        )
        
        # Assertions
        assert isinstance(file_paths, list)
        assert len(file_paths) == 1
        
        # Check that the file exists
        assert os.path.exists(file_paths[0])
        
        # Check that the output file is in the same directory as the input file
        assert os.path.dirname(file_paths[0]) == temp_base_dir
        
        # Check that the content contains the expected response
        with open(file_paths[0], 'r') as f:
            content = f.read()
            assert "madrid" in content.lower() or "Madrid" in content
    finally:
        # Clean up the entire temp directory structure
        if os.path.exists(os.path.dirname(os.path.dirname(temp_base_dir))):
            shutil.rmtree(os.path.dirname(os.path.dirname(temp_base_dir)))


def test_output_extension_only_case():
    """Test that providing only output_extension saves the file in the input file's directory with correct extension."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
    
    # Create a nested temporary directory structure
    temp_base_dir = os.path.join(tempfile.gettempdir(), "agile_team_test_dir", "ext_only_test")
    os.makedirs(temp_base_dir, exist_ok=True)
    
    # Create input file in the nested directory
    input_path = os.path.join(temp_base_dir, "code_prompt.txt")
    with open(input_path, 'w') as f:
        f.write("Write a Python function to calculate the factorial of a number.")
    
    try:
        # Make real API call with only output_extension specified
        file_paths = prompt_from_file_to_file(
            input_path, 
            ["openai:gpt-4o-mini"],
            output_extension="py"  # Only specify extension, no output_dir
        )
        
        # Assertions
        assert isinstance(file_paths, list)
        assert len(file_paths) == 1
        
        # Check that the file exists
        assert os.path.exists(file_paths[0])
        
        # Check that the output file is in the same directory as the input file
        assert os.path.dirname(file_paths[0]) == temp_base_dir
        
        # Check that the file has the requested .py extension
        assert file_paths[0].endswith('.py')
        
        # Check file content contains Python code markers
        with open(file_paths[0], 'r') as f:
            content = f.read()
            assert "def factorial" in content.lower()
    finally:
        # Clean up the entire temp directory structure
        if os.path.exists(os.path.dirname(os.path.dirname(temp_base_dir))):
            shutil.rmtree(os.path.dirname(os.path.dirname(temp_base_dir)))


def test_output_dir_and_extension_case():
    """Test that providing both output_dir and output_extension works correctly."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
    
    # Create a nested temporary directory structure for input and output
    temp_base_dir = os.path.join(tempfile.gettempdir(), "agile_team_test_dir")
    input_dir = os.path.join(temp_base_dir, "input_dir")
    output_dir = os.path.join(temp_base_dir, "output_dir")
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Create input file in the input directory
    input_path = os.path.join(input_dir, "python_prompt.txt")
    with open(input_path, 'w') as f:
        f.write("Write a Python function to calculate the factorial of a number.")
    
    try:
        # Make real API call with both output_dir and output_extension
        file_paths = prompt_from_file_to_file(
            input_path, 
            ["openai:gpt-4o-mini"],
            output_dir=output_dir,
            output_extension="py"
        )
        
        # Assertions
        assert isinstance(file_paths, list)
        assert len(file_paths) == 1
        
        # Check that the file exists
        assert os.path.exists(file_paths[0])
        
        # Check that the output file is in the specified output directory
        assert os.path.dirname(file_paths[0]) == output_dir
        
        # Check that the file has the requested .py extension
        assert file_paths[0].endswith('.py')
        
        # Check file content contains Python code markers
        with open(file_paths[0], 'r') as f:
            content = f.read()
            assert "def factorial" in content.lower()
    finally:
        # Clean up the entire temp directory structure
        if os.path.exists(temp_base_dir):
            shutil.rmtree(temp_base_dir)