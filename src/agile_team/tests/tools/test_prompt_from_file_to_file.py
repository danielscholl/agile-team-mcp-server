"""
Tests for prompt_from_file_to_file functionality.
"""

import pytest
import os
import tempfile
import shutil
import pathlib
import uuid
from dotenv import load_dotenv
from agile_team.tools.prompt_from_file_to_file import prompt_from_file_to_file

# Load environment variables
load_dotenv()

# Use project's directory structure for test files
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
TEST_INPUT_DIR = os.path.join(PROJECT_ROOT, "prompts")
TEST_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "prompts", "responses")

# Create responses directory if it doesn't exist
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)


def test_directory_creation_and_file_writing():
    """Test that the output directory is created and files are written with real API responses with .md extension."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    # Create test input file with a unique name
    test_id = uuid.uuid4().hex[:6]
    input_file_name = f"test_capital_input_{test_id}.txt"
    input_path = os.path.join(TEST_INPUT_DIR, input_file_name)
    
    with open(input_path, 'w') as f:
        f.write("What is the capital of France?")
    
    # Create unique test output directory
    test_output_dir = os.path.join(TEST_OUTPUT_DIR, f"test_output_{test_id}")
    os.makedirs(test_output_dir, exist_ok=True)
    
    file_paths = []
    try:
        # Make real API call
        file_paths = prompt_from_file_to_file(
            input_path, 
            ["openai:gpt-4o-mini"],
            test_output_dir
        )
        
        # Assertions
        assert isinstance(file_paths, list)
        assert len(file_paths) == 1
        
        # Check that the file exists
        assert os.path.exists(file_paths[0])
        
        # Check that the file has a .md extension (based on implementation)
        assert file_paths[0].endswith('.md')
        
        # Check file content contains the expected response
        with open(file_paths[0], 'r') as f:
            content = f.read()
            assert "paris" in content.lower() or "Paris" in content
    finally:
        # Clean up all test files
        if os.path.exists(input_path):
            os.unlink(input_path)
        
        for path in file_paths:
            if os.path.exists(path):
                os.unlink(path)
                
        # Clean up test output directory if it exists
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)


def test_custom_file_extension():
    """Test that the output files use the specified file extension."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    # Create test input file with a unique name
    test_id = uuid.uuid4().hex[:6]
    input_file_name = f"test_factorial_input_{test_id}.txt"
    input_path = os.path.join(TEST_INPUT_DIR, input_file_name)
    
    with open(input_path, 'w') as f:
        f.write("Write a Python function to calculate the factorial of a number.")
    
    # Create unique test output directory
    test_output_dir = os.path.join(TEST_OUTPUT_DIR, f"test_py_output_{test_id}")
    os.makedirs(test_output_dir, exist_ok=True)
    
    file_paths = []
    try:
        # Make real API call with custom extension
        file_paths = prompt_from_file_to_file(
            input_path, 
            ["openai:gpt-4o-mini"],
            test_output_dir,
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
        # Clean up all test files
        if os.path.exists(input_path):
            os.unlink(input_path)
        
        for path in file_paths:
            if os.path.exists(path):
                os.unlink(path)
                
        # Clean up test output directory if it exists
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)


def test_output_path_extension():
    """Test that the extension is extracted correctly from output_path."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    # Create test input file with a unique name
    test_id = uuid.uuid4().hex[:6]
    input_file_name = f"test_output_path_input_{test_id}.txt"
    input_path = os.path.join(TEST_INPUT_DIR, input_file_name)
    
    with open(input_path, 'w') as f:
        f.write("Write a Python function to calculate the factorial of a number.")
    
    # Create unique test output directory
    test_output_dir = os.path.join(TEST_OUTPUT_DIR, f"test_output_path_{test_id}")
    os.makedirs(test_output_dir, exist_ok=True)
    
    # Specify a full output path with a .py extension
    output_path = os.path.join(test_output_dir, "my_factorial_function.py")
    
    file_paths = []
    try:
        # Make real API call with output_path
        file_paths = prompt_from_file_to_file(
            input_path, 
            ["openai:gpt-4o-mini"],
            test_output_dir,
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
        # Clean up all test files
        if os.path.exists(input_path):
            os.unlink(input_path)
        
        for path in file_paths:
            if os.path.exists(path):
                os.unlink(path)
                
        # Clean up test output directory if it exists
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)


def test_exact_output_path():
    """Test that the exact output path is used when specified."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    # Create test input file with a unique name
    test_id = uuid.uuid4().hex[:6]
    input_file_name = f"test_exact_path_input_{test_id}.txt"
    input_path = os.path.join(TEST_INPUT_DIR, input_file_name)
    
    with open(input_path, 'w') as f:
        f.write("Write a Python function to calculate the factorial of a number.")
    
    # Create unique test output directory with nested structure
    test_output_dir = os.path.join(TEST_OUTPUT_DIR, f"test_exact_path_{test_id}", "nested")
    os.makedirs(test_output_dir, exist_ok=True)
    
    # Create a specific output filename that doesn't match the standard naming pattern
    custom_filename = "custom_factorial.py"
    full_output_path = os.path.join(test_output_dir, custom_filename)
    
    file_paths = []
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
        # Clean up all test files
        if os.path.exists(input_path):
            os.unlink(input_path)
        
        for path in file_paths:
            if os.path.exists(path):
                os.unlink(path)
                
        # Clean up test output directory if it exists
        parent_dir = os.path.join(TEST_OUTPUT_DIR, f"test_exact_path_{test_id}")
        if os.path.exists(parent_dir):
            shutil.rmtree(parent_dir)


def test_default_output_directory():
    """Test that the output directory defaults to input file's directory/responses when not specified."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
    
    # Create unique test input directory
    test_id = uuid.uuid4().hex[:6]
    test_input_dir = os.path.join(TEST_INPUT_DIR, f"default_dir_test_{test_id}")
    os.makedirs(test_input_dir, exist_ok=True)
    
    # Create input file in the test input directory
    input_path = os.path.join(test_input_dir, "prompt_file.txt")
    with open(input_path, 'w') as f:
        f.write("What is the capital of Spain?")
    
    file_paths = []
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
        
        # Check that the output file is in the responses subdirectory
        expected_dir = os.path.join(test_input_dir, "responses")
        assert os.path.dirname(file_paths[0]) == expected_dir
        
        # Check that the content contains the expected response
        with open(file_paths[0], 'r') as f:
            content = f.read()
            assert "madrid" in content.lower() or "Madrid" in content
    finally:
        # Clean up all test files
        if os.path.exists(input_path):
            os.unlink(input_path)
        
        for path in file_paths:
            if os.path.exists(path):
                os.unlink(path)
                
        # Clean up test directory if it exists
        if os.path.exists(test_input_dir):
            shutil.rmtree(test_input_dir)


def test_output_extension_only_case():
    """Test that providing only output_extension saves the file in the responses directory with correct extension."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
    
    # Create unique test input directory
    test_id = uuid.uuid4().hex[:6]
    test_input_dir = os.path.join(TEST_INPUT_DIR, f"ext_only_test_{test_id}")
    os.makedirs(test_input_dir, exist_ok=True)
    
    # Create input file in the test input directory
    input_path = os.path.join(test_input_dir, "code_prompt.txt")
    with open(input_path, 'w') as f:
        f.write("Write a Python function to calculate the factorial of a number.")
    
    file_paths = []
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
        
        # Check that the output file is in the responses subdirectory
        expected_dir = os.path.join(test_input_dir, "responses")
        assert os.path.dirname(file_paths[0]) == expected_dir
        
        # Check that the file has the requested .py extension
        assert file_paths[0].endswith('.py')
        
        # Check file content contains Python code markers
        with open(file_paths[0], 'r') as f:
            content = f.read()
            assert "def factorial" in content.lower()
    finally:
        # Clean up all test files
        if os.path.exists(input_path):
            os.unlink(input_path)
        
        for path in file_paths:
            if os.path.exists(path):
                os.unlink(path)
                
        # Clean up test directory if it exists
        if os.path.exists(test_input_dir):
            shutil.rmtree(test_input_dir)


def test_output_dir_and_extension_case():
    """Test that providing both output_dir and output_extension works correctly."""
    # Skip if API keys aren't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
    
    # Create unique test directories
    test_id = uuid.uuid4().hex[:6]
    test_input_dir = os.path.join(TEST_INPUT_DIR, f"dir_ext_input_{test_id}")
    test_output_dir = os.path.join(TEST_OUTPUT_DIR, f"dir_ext_output_{test_id}")
    
    os.makedirs(test_input_dir, exist_ok=True)
    os.makedirs(test_output_dir, exist_ok=True)
    
    # Create input file in the input directory
    input_path = os.path.join(test_input_dir, "python_prompt.txt")
    with open(input_path, 'w') as f:
        f.write("Write a Python function to calculate the factorial of a number.")
    
    file_paths = []
    try:
        # Make real API call with both output_dir and output_extension
        file_paths = prompt_from_file_to_file(
            input_path, 
            ["openai:gpt-4o-mini"],
            output_dir=test_output_dir,
            output_extension="py"
        )
        
        # Assertions
        assert isinstance(file_paths, list)
        assert len(file_paths) == 1
        
        # Check that the file exists
        assert os.path.exists(file_paths[0])
        
        # Check that the output file is in the specified output directory
        assert os.path.dirname(file_paths[0]) == test_output_dir
        
        # Check that the file has the requested .py extension
        assert file_paths[0].endswith('.py')
        
        # Check file content contains Python code markers
        with open(file_paths[0], 'r') as f:
            content = f.read()
            assert "def factorial" in content.lower()
    finally:
        # Clean up all test files
        if os.path.exists(input_path):
            os.unlink(input_path)
        
        for path in file_paths:
            if os.path.exists(path):
                os.unlink(path)
                
        # Clean up test directories
        if os.path.exists(test_input_dir):
            shutil.rmtree(test_input_dir)
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)