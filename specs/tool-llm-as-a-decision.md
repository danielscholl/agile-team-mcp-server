# Feature: LLM as a Decision Maker (Persona DM)

> A tool for team-based decision making using multiple LLM models.

## Implementation Details

The persona_dm tool provides a robust framework for team-based decision making using multiple LLM models:

- Each team member (model) provides a response to the same prompt
- A persona decision model evaluates all responses and provides a final decision
- Responses are generated using the existing prompt_from_file_to_file function
- The persona output is formatted in markdown with a comprehensive explanation

### Core Function Signature

```python
def persona_dm(
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    persona_dm_model: str = DEFAULT_PERSONA_DM_MODEL,
    persona_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
```

#### Parameters

- `from_file`: Path to the file containing the prompt
- `models_prefixed_by_provider`: List of team member models in format "provider:model"
  - If None, defaults to `DEFAULT_TEAM_MODELS`
  - Must include at least two models for decision making
- `output_dir`: Directory where response files should be saved
  - If None, defaults to input file's directory/responses
- `output_extension`: File extension for output files (e.g., 'py', 'txt', 'md')
  - If None, defaults to 'md'
- `output_path`: Optional full output path with filename for the persona document
  - If provided, overrides output_dir and output_extension for the persona file
- `persona_dm_model`: Model to use for making the decision
  - Defaults to "openai:o4-mini"
- `persona_prompt`: Custom persona prompt template
  - If None, uses the DEFAULT_PERSONA_PROMPT

#### Return Value

- Path to the persona output file as a string

### Default Values

```python
# Default persona decision model
DEFAULT_PERSONA_DM_MODEL = "openai:o4-mini"

# Default team member models
DEFAULT_TEAM_MODELS = ["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"]
```

### Persona Prompt Template

The persona prompt uses an XML-style format with placeholders:

```xml
<purpose>
    You are the decision maker of the agile team. You are given a list of responses from your team members. Your job is to take in the original question prompt, and each of the team members' responses, and choose the best direction for the team.
</purpose>
<instructions>
    <instruction>Each team member has proposed an answer to the question posed in the prompt.</instruction>
    <instruction>Given the original question prompt, and each of the team members' responses, choose the best answer.</instruction>
    <instruction>Tally the votes of the team members, choose the best direction, and explain why you chose it.</instruction>
    <instruction>To preserve anonymity, we will use model names instead of real names of your team members. When responding, use the model names in your response.</instruction>
    <instruction>As a decision maker, you breakdown the decision into several categories including: risk, reward, timeline, and resources. In addition to these guiding categories, you also consider the team members' expertise and experience. As a bleeding edge decision maker, you also invent new dimensions of decision making to help you make the best decision for your company.</instruction>
    <instruction>Your final decision maker response should be in markdown format with a comprehensive explanation of your decision. Start the top of the file with a title that says "Team Decision", include a table of contents, briefly describe the question/problem at hand then dive into several sections. One of your first sections should be a quick summary of your decision, then breakdown each of the team members' decisions into sections with your commentary on each. Where we lead into your decision with the categories of your decision making process, and then we lead into your final decision.</instruction>
</instructions>

<original-question>{original_prompt}</original-question>

<team-decisions>
{team_responses}
</team-decisions>
```

### Implementation Logic

1. **Input Validation**:
   - If no team models are provided, use `DEFAULT_TEAM_MODELS`
   - Ensure at least two team member models are provided for decision making
   - Validate persona model using `validate_and_correct_models`

2. **File Path Handling**:
   - Handle different combinations of output_dir, output_path, and output_extension
   - Calculate appropriate output directory for team member responses
   - Create output directories if they don't exist

3. **Team Responses**:
   - Use prompt_from_file_to_file to generate responses from each team member
   - Read original prompt from the input file
   - Parse and format team responses for the persona prompt
   - Skip error files when collecting team responses

4. **Persona Decision Generation**:
   - Format the persona prompt with original question and team responses
   - Call the persona model using prompt_model
   - Format persona output with appropriate naming based on input filename
   - Write the persona decision to the specified output path

5. **Error Handling**:
   - Catch and handle file read/write errors
   - Create error files with appropriate naming in case of failures
   - Raise meaningful exceptions with detailed error messages

### MCP Tool Registration

The persona decision maker is registered as an MCP tool in server.py:

```python
@mcp.tool()
def persona_dm_tool(
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    persona_dm_model: str = DEFAULT_PERSONA_DM_MODEL, 
    persona_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
    """
    Generate responses from multiple LLM models and use a decision maker model to choose the best direction.
    
    This tool first sends a prompt from a file to multiple models, then uses a designated
    decision maker model to evaluate all responses and provide a final decision.
    
    Args:
        from_file: Path to the file containing the prompt text
        models_prefixed_by_provider: List of team member models in format "provider:model" 
                                    (if None, defaults to ["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"])
        output_dir: Directory where response files should be saved (defaults to input file's directory/responses)
        output_extension: File extension for output files (e.g., 'py', 'txt', 'md')
        output_path: Optional full output path with filename for the persona document
        persona_dm_model: Model to use for making the decision (defaults to "openai:o4-mini")
        persona_prompt: Custom persona prompt template (if None, uses the default)
    
    Returns:
        Path to the persona output file
    """
    return persona_dm(...)
```

## Relevant Files

- src/agile_team/server.py - MCP server tool registration
- src/agile_team/tools/persona_dm.py - Core implementation
- src/agile_team/tools/prompt_from_file_to_file.py - Used to generate team responses
- src/agile_team/shared/model_router.py - Used for model validation and prompting
- src/agile_team/shared/utils.py - File operations and utilities
- src/agile_team/tests/tools/test_persona_dm.py - Test cases

## Testing Requirements

Tests should cover:
- Basic functionality with multiple models
- Parameter validation (minimum 2 models required)
- Various output path configurations
- Custom persona prompt template usage
- Error handling for invalid models
- Error handling for file operations

## Validation

- Run tests with `uv run pytest src/agile_team/tests/tools/test_persona_dm.py`
- Verify end-to-end functionality with sample prompts
- Validate MCP tool registration with `uv run agile-team --help`