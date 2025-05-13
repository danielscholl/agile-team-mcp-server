# MCP Server Tool Spec – Model Wrapper

> A lightweight wrapper MCP server for OpenAI, Anthropic, Gemini, Groq, DeepSeek, and Ollama.

## Required Implementation Tasks

- [ ] ✅ Implement prompt routing and model selection for all supported providers
- [ ] ✅ Build robust error handling for all possible failure scenarios
- [ ] ✅ Ensure all tools are registered and callable via MCP in `server.py`
- [ ] ✅ Validate and correct model/provider names using the "magic" weak_provider_and_model function
- [ ] ✅ For OpenAI o-series models (o3-mini, o4-mini, o3), support reasoning effort suffixes (`:low`, `:medium`, `:high`).
- [ ] ✅ For Anthropic Claude models, support thinking token budget suffixes (`:4k`, `:16k`, etc.)

### Tool Details

- Implemented in `src/agile_team/` as described in the codebase structure below
- **prompt(text, models_prefixed_by_provider: List[str]) -> List[str]**
  - Validates that each entry in `models_prefixed_by_provider` matches the format `<provider>:<model>`
  - Routes the prompt to the correct provider/model, correcting the model if needed using the "magic" function
  - Returns a list of responses, one per model
- **prompt_from_file(file, models_prefixed_by_provider: List[str]) -> List[str]**
  - Reads prompt from file, then routes as above
- **prompt_from_file_to_file(file, models_prefixed_by_provider: List[str], output_dir: str = None, output_extension: str = None, output_path: str = None) -> List[str]**
  - Reads prompt from file, runs for each model, writes responses to files
  - Supports custom output directory, extension, and full path specification
  - Returns list of file paths
- **list_providers() -> Dict**
  - Returns all supported providers with both long names and short aliases
  - Returns providers in a structured dictionary format
- **list_models(provider: str) -> List[str]**
  - Returns all models for the given provider using the provider's list_models() function
  - Handles provider name correction (short aliases, etc.)

#### Model Correction Logic

- Provider name correction:
  - Supports full names (e.g., "openai") and single-letter shortcuts (e.g., "o")
  - Maps shortcuts to full provider names using `SHORT_NAME_MAPPING`
  - Uses `ModelProviders` enum to maintain the mapping
- Model name correction:
  - Uses fuzzy matching for inexact model names via `weak_provider_and_model` function
  - Checks if model name is contained within available model names or vice versa
  - Falls back to first available model if no match is found
  - Logs corrections for debugging purposes

#### Special Model Features

1. **OpenAI Reasoning Effort**:
   - Supports `:low`, `:medium`, `:high` suffixes for specific models
   - Only enabled for models in `REASONING_ENABLED_MODELS = ["o3-mini", "o4-mini", "o3"]`
   - Implementation passes reasoning_effort parameter directly to OpenAI API

2. **Anthropic Thinking**:
   - Supports thinking token budget suffixes (e.g., `:4k` or `:16000`)
   - Values < 100 are interpreted as "k" (multiplied by 1024)
   - Values are clamped between 1024-16000 tokens
   - Implementation adds 1000 tokens to max_tokens parameter for response
   - Available primarily for `claude-3-7-sonnet-20250219` model

3. **Gemini Thinking**:
   - Similar to Anthropic, with provider-specific range limitations
   - Handles different Google Gemini API versions

### Input Rules

- `models_prefixed_by_provider` must be a list of strings in the format `<provider>:<model>` or `<provider-short>:<model>`
- Providers must be one of the supported long or short names
- All input must be validated; raise errors for invalid formats
- Model suffixes (reasoning, thinking) must be appended with a colon (`:`)

### Testing Requirements

- Use real API calls (no mocking)
- Use `.env.sample` and `load_dotenv()` in tests to load API keys
- Add test coverage for:
  - Each provider and at least one model per provider
  - Model correction logic (test with both valid and invalid model names)
  - Input validation errors
  - API/network errors
  - Special features (reasoning levels, thinking budget)
- For prompt tests, use: "What is the capital of France?" and expect "Paris" (case-insensitive)
- For list_models/list_providers, verify expected output structure

### OpenAI Reasoning Levels (o-series)

For OpenAI o-series models (`o3-mini`, `o4-mini`, `o3`), support reasoning effort suffixes (`:low`, `:medium`, `:high`).
- If a model is specified with one of these suffixes (e.g., `o4-mini:high`), route the prompt to the reasoning-enabled API call
- If no suffix is present, use the standard prompt function
- Suffix parsing and routing fully implemented and tested
- Valid model names: `o4-mini:low`, `o4-mini:medium`, `o4-mini:high`, etc.

### Anthropic Extended Thinking

For Anthropic Claude models, support thinking token budget suffixes.
- Format: `<model>:<tokens>k` or `<model>:<tokens>`
- Examples: `claude-3-7-sonnet-20250219:4k`, `claude-3-7-sonnet-20250219:16000`
- Values < 100 are interpreted as "k" (multiplied by 1024)
- Values are clamped between 1024-16000 tokens

## Tools to Expose

```text
prompt(
    text: str,
    models_prefixed_by_provider: List[str] = None
) -> List[str]

prompt_from_file(
    file_path: str,
    models_prefixed_by_provider: List[str] = None
) -> List[str]

prompt_from_file_to_file(
    file_path: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None
) -> List[str]

list_providers() -> Dict

list_models(provider: str) -> List[str]
```

### Response Format

- Success:
  ```python
  {
    "tool_name": "<tool>",
    "status": "success",
    "result": { ... }
  }
  ```
- Error:
  ```python
  {
    "tool_name": "<tool>",
    "status": "error",
    "error": {
        "code": str,  # One of the ErrorCode enum values
        "message": str
    }
  }
  ```

### Error Codes

| Code | Meaning |
|------|---------|
| INVALID_INPUT_FORMAT | Malformed input or model/provider string |
| MISSING_PARAMETER    | Required parameter missing |
| PROVIDER_NOT_FOUND   | Provider not supported |
| MODEL_NOT_FOUND      | Model not found for provider |
| API_ERROR            | Upstream provider API/network error |
| INTERNAL_SERVER_ERROR| Unhandled server exception |

## Provider Details

| Provider | Short Prefix | Full Prefix | Example Usage |
|----------|--------------|-------------|--------------|
| OpenAI   | `o`          | `openai`    | `o:gpt-4o-mini` or `o:o4-mini:high` |
| Anthropic | `a`         | `anthropic` | `a:claude-3-5-haiku` or `a:claude-3-7-sonnet:4k` |
| Google Gemini | `g`     | `gemini`    | `g:gemini-2.5-pro-exp-03-25` |
| Groq     | `q`          | `groq`      | `q:llama-3.1-70b-versatile` |
| DeepSeek | `d`          | `deepseek`  | `d:deepseek-coder` |
| Ollama   | `l`          | `ollama`    | `l:llama3.1` |

## Codebase Structure

- .env.sample
- src/
    - agile_team/                   # Main package directory
        - __init__.py
        - main.py             # Entry point for the application
        - server.py           # FastMCP instance creation and tool registration
        - tools/
            - __init__.py
            - prompt.py
            - prompt_from_file.py
            - prompt_from_file_to_file.py
            - list_providers.py
            - list_models.py
        - shared/
            - __init__.py
            - utils.py        # Helper functions for formatting, error handling, etc.
            - data_types.py   # Pydantic models for request/response validation
            - validator.py
            - model_router.py
            - llm_providers/
                - __init__.py
                - openai.py
                - anthropic.py
                - gemini.py
                - groq.py
                - deepseek.py
                - ollama.py
                - testing.py
        - tests/
            - __init__.py
            - tools/
                - __init__.py
                - test_prompt.py
                - test_prompt_from_file.py
                - test_prompt_from_file_to_file.py
                - test_list_providers.py
                - test_list_models.py
            - shared/
                - __init__.py
                - test_utils.py
                - test_validator.py
                - test_model_router.py
                - llm_providers/
                    - __init__.py
                    - test_openai.py
                    - test_anthropic.py
                    - test_gemini.py
                    - test_groq.py
                    - test_deepseek.py
                    - test_ollama.py

## Per Provider Documentation

- See `ai_docs/llm_providers_details.xml` for details on each provider's API and authentication.

## Validation (close the loop)

- Run `uv run pytest <path_to_test>` iteratively as you build out the tests.
- After code is written, run `uv run pytest` to validate all tests are passing.
- At the end, use `uv run agile-team --help` to validate the MCP server works.