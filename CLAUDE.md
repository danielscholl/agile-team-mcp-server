# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

The Agile Team MCP Server is a service that provides a unified interface to multiple Large Language Model (LLM) providers. It allows sending prompts to various LLMs through a consistent API, handling model name validation and correction, and supports multiple tools for different workflows including team decision-making.

## Setup and Installation

```bash
# Clone the repository
git clone https://github.com/danielscholl/agile-team-mcp-server.git
cd agile-team-mcp-server

# Install dependencies using uv
uv sync
uv pip install -e .

# Setup environment variables for API keys
cp .env.sample .env
# Edit .env file with your API keys
```

## Environment Configuration

The server requires API keys for various LLM providers:

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OLLAMA_HOST=http://localhost:11434
```

## Development Commands

```bash
# Run tests
uv run pytest

# Run tests with test coverage
uv run pytest --cov=agile_team

# Run specific test file or test
uv run pytest src/agile_team/tests/tools/test_prompt.py
uv run pytest src/agile_team/tests/tools/test_prompt.py::test_prompt_basic

# Run the MCP server
uv run agile-team
```

## Architecture Overview

The project has the following structure:

1. **Server Layer**: Implemented in `server.py`, this creates a FastMCP server and registers MCP tools. It handles the HTTP interface and tool registration.

2. **Tool Layer**: Tools in the `tools/` directory implement specific functionalities:
   - `prompt.py`: Sends text prompts to models
   - `prompt_from_file.py`: Sends prompts from files
   - `prompt_from_file_to_file.py`: Sends prompts from files and saves responses to files
   - `list_providers.py`: Lists available LLM providers
   - `list_models.py`: Lists available models for a provider
   - `persona_dm.py`: Implements team decision-making with multiple LLMs

3. **Provider Layer**: In `shared/llm_providers/`, each file implements a provider interface:
   - `openai.py`, `anthropic.py`, `gemini.py`, etc. handle API calls to specific providers
   - Each provider has a `prompt()` function to send prompts to models
   - Each provider implements provider-specific features (e.g., reasoning effort for OpenAI)

4. **Shared Services**:
   - `model_router.py`: Routes requests to appropriate providers
   - `validator.py`: Validates and corrects provider/model names
   - `utils.py`: Common utilities
   - `data_types.py`: Pydantic models for data validation

## Key Design Patterns

1. **Model Routing**: The `ModelRouter` class dynamically imports provider modules based on the requested provider name, enabling a clean separation between providers.

2. **Provider Normalization**: Short names like "o" are automatically mapped to full names like "openai", making the API user-friendly while maintaining internal consistency.

3. **Tool Registration**: Each MCP tool is registered with the FastMCP server using decorators, providing a clean interface for adding new tools.

4. **Persona Decision Making**: The `persona_dm` tool implements a team decision-making pattern, where multiple LLMs generate responses and a decision-maker LLM chooses the best approach.

## Testing

The test suite is organized to match the main code structure:
- Tests for providers in `tests/shared/llm_providers/`
- Tests for tools in `tests/tools/`
- Tests for shared services in `tests/shared/`

Many tests require valid API keys to run and will skip if the relevant keys are not available.