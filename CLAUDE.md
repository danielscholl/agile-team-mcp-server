# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Installation and Setup

```bash
# Clone and install
git clone https://github.com/danielscholl/agile-team-mcp-server.git
cd agile-team-mcp-server
uv sync

# Install in development mode
uv pip install -e .

# Configure environment variables by copying template and editing
cp .env.sample .env
# Edit .env to add your API keys
```

### Testing

```bash
# Run all tests
uv run pytest

# Run tests for a specific module
uv run pytest src/agile_team/tests/shared/test_model_router.py

# Run a specific test
uv run pytest src/agile_team/tests/shared/test_model_router.py::test_list_providers
```

### Running the Server

```bash
# Run the server locally
uv run agile-team
```

## Project Architecture

This project is an MCP (Model Control Protocol) server that provides a unified interface to interact with multiple LLM providers. It serves as an intermediary between clients and various LLM services, standardizing the interface to access models from different providers.

### Core Components

1. **MCP Server Interface** (`server.py`): 
   - Initializes a FastMCP server instance and registers tool functions that clients can use to interact with LLMs
   - Provides tools for sending prompts, reading from files, and listing providers/models

2. **Model Router** (`shared/model_router.py`):
   - Central component that routes requests to the appropriate provider
   - Manages provider configuration and API key validation
   - Provides dynamic model discovery
   - Handles provider and model name corrections

3. **LLM Provider Implementations** (`shared/llm_providers/`):
   - Separate modules for each supported provider (OpenAI, Anthropic, Gemini, etc.)
   - Each provider module implements standard interfaces:
     - `prompt()`: Send a prompt to a model and get a response
     - `list_models()`: List available models for the provider
   - Providers can also implement special features like extended thinking for Anthropic

4. **Tools** (`tools/`):
   - Client-facing tools for interacting with LLMs:
     - `prompt.py`: Send a prompt to one or more LLMs
     - `prompt_from_file.py`: Read a prompt from a file and send it to LLMs
     - `prompt_from_file_to_file.py`: Process a file and write responses to output files
     - `list_providers.py`/`list_models.py`: Discovery tools for available providers/models

5. **Shared Utilities** (`shared/`):
   - `data_types.py`: Pydantic models for request validation
   - `utils.py`: Helper functions for file operations, model name parsing, etc.
   - `validator.py`: Input validation and correction logic

### Provider Integration Pattern

The system follows a consistent pattern for integrating LLM providers:

1. Define provider in `ModelProviders` enum (`data_types.py`)
2. Configure provider in `PROVIDER_CONFIG` dictionary (`model_router.py`)
3. Implement provider module with standard interface (`llm_providers/provider.py`)
4. Provider module automatically loaded by `ModelRouter` when needed

### Special Features

1. **Model Name Correction**: The system attempts to correct typos or variations in provider and model names
2. **Thinking and Reasoning Control**: Support for controlling model reasoning through suffixes:
   - Extended thinking for Claude (e.g., `claude-3-7-sonnet:4k`)
   - Reasoning effort levels for some models (e.g., `model:high`)
3. **File-Based Operations**: Tools to read prompts from files and write responses to files