# MCP Server Tool Spec – Model Wrapper

> A lightweight wrapper MCP server for OpenAI, Anthropic, Gemini, Groq, DeepSeek, and Ollama.

## Required Implementation Tasks

- [ ] ⚠️ Implement prompt routing and model selection for all supported providers
- [ ] ⚠️ Build robust error handling for all possible failure scenarios
- [ ] ⚠️ Ensure all tools are registered and callable via MCP in `server.py`
- [ ] ⚠️ Validate and correct model/provider names using the "magic" weak_provider_and_model function
- [ ] ⚠️ For OpenAI o-series models (o3-mini, o4-mini, o3), support reasoning effort suffixes (`:low`, `:medium`, `:high`). If present, route to a `prompt_with_thinking` function (see ai_docs/openai-reasoning-effort.md for details); otherwise, use the standard prompt function. Validate this feature with tests.

### Tool Details

- Implement in `src/agile-team/` as described in the codebase structure below
- **prompt(text, models_prefixed_by_provider: List[str]) -> List[str>**
  - Validate that each entry in `models_prefixed_by_provider` matches the format `<provider>:<model>`
  - Route the prompt to the correct provider/model, correcting the model if needed using the "magic" function
  - Return a list of responses, one per model
- **prompt_from_file(file, models_prefixed_by_provider: List[str]) -> List[str>**
  - Read prompt from file, then route as above
- **prompt_from_file_to_file(file, models_prefixed_by_provider: List[str], output_dir: str = ".") -> List[str>**
  - Read prompt from file, run for each model, write responses to files in `output_dir`, return list of file paths
- **list_providers() -> List[str>**
  - Return all supported providers (long and short names)
- **list_models(provider: str) -> List[str>**
  - Return all models for the given provider using the provider’s list_models() function

#### Model Correction Logic

- If a model in `models_prefixed_by_provider` is not found in the provider’s list, use the "magic" function to correct it by prompting the model itself with the available list.
- Log the original, corrected, and used model/provider to the console.

### Input Rules

- `models_prefixed_by_provider` must be a list of strings in the format `<provider>:<model>`
- Providers must be one of the supported long or short names
- All input must be validated; raise errors for invalid formats

### Testing Requirements

- Use real API calls (no mocking)
- Use `.env.sample` and `load_dotenv()` in tests to load API keys
- Add test coverage for:
  - Each provider and at least one model per provider
  - Model correction logic (test with both valid and invalid model names)
  - Input validation errors
  - API/network errors
- For prompt tests, use: "What is the capital of France?" and expect "Paris" (case-insensitive)
- For list_models/list_providers, verify expected output structure

### OpenAI Reasoning Levels (o-series)

For OpenAI o-series models (`o3-mini`, `o4-mini`, `o3`), support reasoning effort suffixes (`:low`, `:medium`, `:high`).
- If a model is specified with one of these suffixes (e.g., `o4-mini:high`), route the prompt to a `prompt_with_thinking` function (see `ai_docs/openai-reasoning-effort.md` for details).
- If no suffix is present, use the standard prompt function.
- Suffix parsing and routing must be implemented and validated with tests.
- Valid model names: `o4-mini:low`, `o4-mini:medium`, `o4-mini:high`, etc.
- Add test coverage for all suffixes and fallback logic.

## Tools to Expose

```text
prompt(
    text: str,
    models_prefixed_by_provider: List[str]
) -> List[str]

prompt_from_file(
    file: str,
    models_prefixed_by_provider: List[str]
) -> List[str]

prompt_from_file_to_file(
    file: str,
    models_prefixed_by_provider: List[str],
    output_dir: str = "."
) -> List[str]

list_providers() -> List[str>

list_models(provider: str) -> List[str>
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

## Codebase Structure

- .env.sample
- src/
    - just_prompt/                   # Main package directory with your server name
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
            - ... (other tool files as needed)
        - shared/
            - __init__.py
            - utils.py        # Helper functions for formatting, error handling, etc.
            - data_types.py   # Pydantic models for request/response validation
            - validator.py
            - model_router.py
        - tests/
            - __init__.py
            - tools/
                - __init__.py
                - test_prompt.py
                - test_prompt_from_file.py
                - test_prompt_from_file_to_file.py
                - test_list_providers.py
                - test_list_models.py
                - ... (other tool tests as needed)
            - shared/
                - __init__.py
                - test_utils.py

## Per Provider Documentation

- See `ai_docs/llm_providers_details.xml` for details on each provider’s API and authentication.

## Validation (close the loop)

- Run `uv run pytest <path_to_test>` iteratively as you build out the tests.
- After code is written, run `uv run pytest` to validate all tests are passing.
- At the end, use `uv run just-prompt --help` to validate the MCP server works.

