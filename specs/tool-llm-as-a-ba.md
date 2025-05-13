# Feature: LLM as a Business Analyst (Persona BA)

> A tool for performing tasks typically handled by a Business Analyst, with optional decision-making integration.

## Implementation Details

The persona_ba tool provides a specialized analysis framework using a Business Analyst persona, built on a reusable persona architecture:

- Creates a base persona function to handle common functionality for all personas
- Leverages a specialized Business Analyst prompt template to analyze business requirements
- Efficiently integrates with the persona_dm tool for team-based decision making
- Returns detailed business analysis formatted in markdown

### Centralized Model Configuration

To maintain consistency across the application, we'll implement a centralized configuration module:

```python
# In src/agile_team/shared/config.py
"""Centralized configuration for the Agile Team MCP Server."""

# Default single model for all tools
DEFAULT_MODEL = "openai:gpt-4o-mini"

# Default team models for multi-model scenarios
DEFAULT_TEAM_MODELS = ["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"]

# Default decision maker model
DEFAULT_DECISION_MAKER_MODEL = "openai:gpt-4o-mini"  # Uses the same default as standard operations
```

All tools will import these settings from the central config file, ensuring consistency throughout the application.

### Reusable Persona Architecture

To enable easy onboarding of multiple personas, we'll implement a base persona function that all specific personas can use:

```python
def persona_base(
    persona_name: str,
    persona_prompt: str,
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    use_decision_maker: bool = False,
    decision_maker_models: List[str] = None,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
```

Then each specific persona becomes a lightweight wrapper around this base function:

```python
def persona_ba(
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    use_decision_maker: bool = False,
    decision_maker_models: List[str] = None,
    ba_prompt: str = DEFAULT_BA_PROMPT,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
    """
    Business Analyst persona implementation.
    """
    return persona_base(
        persona_name="business_analyst",
        persona_prompt=ba_prompt,
        from_file=from_file,
        models_prefixed_by_provider=models_prefixed_by_provider,
        output_dir=output_dir,
        output_extension=output_extension,
        output_path=output_path,
        use_decision_maker=use_decision_maker,
        decision_maker_models=decision_maker_models,
        decision_maker_model=decision_maker_model,
        decision_maker_prompt=decision_maker_prompt
    )
```

### Core Function Signatures

#### Base Persona Function

```python
def persona_base(
    persona_name: str,
    persona_prompt: str,
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    use_decision_maker: bool = False,
    decision_maker_models: List[str] = None,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
```

#### Business Analyst Persona

```python
def persona_ba(
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    use_decision_maker: bool = False,
    decision_maker_models: List[str] = None,
    ba_prompt: str = DEFAULT_BA_PROMPT,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
```

### Business Analyst Prompt Template

```xml
<purpose>
    You are a world-class expert Market & Business Analyst and also the best research assistant I have ever met, possessing deep expertise in both comprehensive market research and collaborative project definition. 
    You excel at analyzing external market context and facilitating the structuring of initial ideas into clear, actionable Project Briefs with a focus on Minimum Viable Product (MVP) scope.
</purpose>

<capabilities>
    <capability>Data analysis and business needs understanding</capability>
    <capability>Market opportunity and pain point identification</capability>
    <capability>Competitor analysis</capability>
    <capability>Target audience definition</capability>
    <capability>Clear communication and structured dialogue</capability>
</capabilities>

<modes>   
    <mode>
        <n>Project Briefing Mode</n>
        <description>Collaboratively guide the user through brainstorming and definition</description>
        <outputs>
            <o>Core Problem</o>
            <o>Goals</o>
            <o>Audience</o>
            <o>Core Concept/Features (High-Level)</o>
            <o>MVP Scope (In/Out)</o>
            <o>Initial Technical Leanings (Optional)</o>
        </outputs>
        <tone>Detailed, knowledgeable, structured, professional</tone>
    </mode>
</modes>

<instructions>
    <instruction>Identify the required mode (Market Research or Project Briefing) based on the user's request. If unclear, assume Project Briefing Mode.</instruction>
    <instruction>For Market Research Mode: Focus on executing deep research based on the provided concept. Present findings clearly and concisely in the final report.</instruction>
    <instruction>For Project Briefing Mode: Engage in analysis of the concept, problem, goals, users, and MVP scope.</instruction>
    <instruction>Use structured formats (lists, sections) for outputs and avoid ambiguity.</instruction>
    <instruction>Ensure your project brief is well-structured, clear, and actionable.</instruction>
    <instruction>Prioritize understanding user needs and project goals.</instruction>
    <instruction>Be capable of explaining market concepts or analysis techniques clearly if requested.</instruction>
    <instruction>Create a project brief that is well-structured, just like a real business analyst would.</instruction>
    <instruction>Do not include any metadata, headers, footers, or formatting that isn't part of the actual project brief.</instruction>
    <instruction>Do not ask additional questions, just provide the requested output.</instruction>
</instructions>

<interaction-flow>
    <step>Identify Mode: Determine if the user needs Market Research or Project Briefing</step>
    <step>Input Analysis: Analyze the provided information based on the identified mode</step>
    <step>Execution: Perform research or guide through project definition</step>
    <step>Output Generation: Structure findings into appropriate format</step>
    <step>Presentation: Present final report or Project Brief document</step>
</interaction-flow>

<analyst-request>{analyst_request}</analyst-request>
```

### Implementation Logic

1. **Base Persona Function Implementation**:
   - Common parameter handling and validation
   - Uses centralized model configuration
   - Single-model and decision maker workflows
   - File path and error handling logic

2. **Single Model Flow** (when `use_decision_maker` is False):
   - If no model specified, uses DEFAULT_MODEL
   - Reads prompt from file
   - Formats with persona template
   - Sends to specified model
   - Saves and returns output path

3. **Decision Maker Flow** (when `use_decision_maker` is True):
   - If no decision maker models specified, uses DEFAULT_TEAM_MODELS
   - Creates a temporary prompt file with the persona prompt and original prompt contents
   - Leverages existing `persona_dm` function to handle the team decision process
   - Uses DEFAULT_DECISION_MAKER_MODEL if no decision maker model specified
   - Returns the decision maker result path

4. **File Path Handling**:
   - File naming based on persona name and model details
   - Consistent with existing file path conventions in other tools

### MCP Tool Registration

Register the Business Analyst tool in server.py:

```python
@mcp.tool()
def persona_ba_tool(
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    use_decision_maker: bool = False,
    decision_maker_models: List[str] = None,
    ba_prompt: str = DEFAULT_BA_PROMPT,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
    """
    Generate business analysis using a specialized Business Analyst persona, with optional decision making.
    
    This tool uses a specialized Business Analyst prompt to analyze business requirements
    from a file. It can either use a single model or leverage the team decision-making
    functionality to get multiple perspectives and consolidate them.
    
    Args:
        from_file: Path to the file containing the business requirements
        models_prefixed_by_provider: List of models in format "provider:model"
                                    (if None, defaults to DEFAULT_MODEL)
        output_dir: Directory where response files should be saved (defaults to input file's directory/responses)
        output_extension: File extension for output files (e.g., 'py', 'txt', 'md')
        output_path: Optional full output path with filename for the output document
        use_decision_maker: Whether to use the decision maker functionality
        decision_maker_models: Models to use if use_decision_maker is True
                             (if None, defaults to DEFAULT_TEAM_MODELS)
        ba_prompt: Custom business analyst prompt template
        decision_maker_model: Model to use for decision making (defaults to DEFAULT_DECISION_MAKER_MODEL)
        decision_maker_prompt: Custom persona prompt template for decision making
    
    Returns:
        Path to the business analysis output file
    """
    return persona_ba(
        from_file=from_file,
        models_prefixed_by_provider=models_prefixed_by_provider,
        output_dir=output_dir,
        output_extension=output_extension,
        output_path=output_path,
        use_decision_maker=use_decision_maker,
        decision_maker_models=decision_maker_models,
        ba_prompt=ba_prompt,
        decision_maker_model=decision_maker_model,
        decision_maker_prompt=decision_maker_prompt
    )
```

## Relevant Files

- src/agile_team/shared/config.py - New file for centralized configuration
- src/agile_team/server.py - Updated to use centralized configuration
- src/agile_team/tools/persona_base.py - New file with core reusable persona logic
- src/agile_team/tools/persona_ba.py - Business Analyst persona implementation
- src/agile_team/tools/persona_dm.py - Updated to use centralized configuration
- src/agile_team/shared/model_router.py - Used for model validation and prompting
- src/agile_team/shared/utils.py - File operations and utilities
- src/agile_team/tests/tools/test_persona_base.py - Test cases for base functionality
- src/agile_team/tests/tools/test_persona_ba.py - Test cases for BA implementation

## Testing Requirements

Tests should cover:
- Base persona functionality in isolation
- Business Analyst implementation 
- Integration with decision maker when use_decision_maker is True
- Parameter validation and error handling
- Various output path configurations
- Custom prompt template usage

## Validation

- Run tests with `uv run pytest src/agile_team/tests/tools/test_persona_ba.py`
- Verify end-to-end functionality with sample prompts
- Validate MCP tool registration with `uv run agile-team --help`
- Update README.md with documentation for the new tool

## Future Persona Implementation

This architecture makes it easy to add additional personas in the future:

```python
def persona_product_manager(...):
    return persona_base(
        persona_name="product_manager",
        persona_prompt=DEFAULT_PM_PROMPT,
        ...
    )

def persona_data_scientist(...):
    return persona_base(
        persona_name="data_scientist",
        persona_prompt=DEFAULT_DS_PROMPT,
        ...
    )
```