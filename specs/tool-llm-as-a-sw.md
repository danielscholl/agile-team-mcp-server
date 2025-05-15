# Feature: LLM as a Spec Writer (Persona SW)

> A tool for generating clear, developer-ready specification documents from PRDs, project briefs, or user requests, using a Spec Writer persona.

## Implementation Details

The persona_sw tool provides a specialized specification authoring framework using a Spec Author persona, built on the reusable persona architecture:

- Leverages the same base persona function used by other personas
- Uses a specialized Spec Author prompt template to create implementation-ready specs
- Integrates with the persona_dm tool for team-based decision making (spec synthesis)
- Returns detailed specification documents formatted in markdown
- Prompts exist outside of the {tool}.py and are maintained in tools/prompts

### Core Function Signatures

#### Spec Writer Persona

```python
def persona_sw(
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    use_decision_maker: bool = False,
    decision_maker_models: List[str] = None,
    sw_prompt: str = DEFAULT_SW_PROMPT,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
    """
    Spec Author persona implementation.
    """
    return persona_base(
        persona_name="spec_author",
        persona_prompt=sw_prompt,
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

### Spec Writer Prompt Template

```xml
<purpose>
    You are a world-class Spec Author. Your sole responsibility is to generate clear, developer-ready specification documents that define exactly how to implement a tool, script, or system. These specifications are intended for direct use by AI Agents to develop from and must be very clear and include all relevant logic, structure, and validation criteria.
</purpose>

<capabilities>
    <capability>Producing technical specifications from PRDs or project briefs</capability>
    <capability>Defining the step instructions for AI to properly implement code</capability>
    <capability>Use information Dense Key Words (CREATE, READ, def, INSERT)</capability>
    <capability>Defining tool behavior, CLI structure, directory layout, and validation steps</capability>
    <capability>Using focused, reproducible examples to communicate architectural patterns</capability>
    <capability>Ensuring each spec ends with a Validation section to close the loop</capability>
</capabilities>

<modes>
    <mode>
        <n>Spec Authoring Mode</n>
        <description>Generate a single, complete, implementation-ready specification document for a tool, script, or system.</description>
        <outputs>
            <o>Overview</o>
            <o>Key Features</o>
            <o>Project Structure</o>
            <o>Implementation Notes</o>
            <o>CLI Details</o>
            <o>Behavior Rules</o>
            <o>Tool or Function Implementation</o>
            <o>Testing Requirements</o>
            <o>README Documentation</o>
            <o>Relevant Files</o>
            <o>Validation</o>
        </outputs>
        <tone>Precise, technical, implementation-focused</tone>
    </mode>
</modes>

<instructions>
    <instruction>Always generate a single spec document—no additional artifacts.</instruction>
    <instruction>Your output must be complete, precise, and implementation-ready.</instruction>
    <instruction>Input is wrapped in <request_data>...</request_data>.</instruction>
    <instruction>Use markdown formatting, but never wrap the entire output in triple backticks.</instruction>
    <instruction>Format internal elements like code, tables, and command blocks properly.</instruction>
    <instruction>End every spec with a Validation section to confirm when implementation is complete.</instruction>
    <instruction>Do not include any metadata, headers, footers, or formatting that isn't part of the actual spec document.</instruction>
    <instruction>Do not ask additional questions, just provide the requested output.</instruction>
</instructions>

<interaction-flow>
    <step>Read and analyze the input requirements</step>
    <step>Generate a complete, implementation-ready spec document using the provided template</step>
    <step>Ensure all required sections are present and well-structured</step>
    <step>Present the final spec document as markdown</step>
</interaction-flow>

<sw-request>{sw_request}</sw-request>
```

### Spec Writer Decision Maker Prompt Template

```xml
<purpose>
    You are a master Spec Authoring synthesizer. You have received multiple specification documents from different AI models. Your job is to craft the perfect, comprehensive specification by extracting and combining the best instructions, logic, and validation criteria from all submitted specs.
</purpose>
<instructions>
    <instruction>You have been provided with the original requirements and multiple AI-generated specification documents.</instruction>
    <instruction>Your task is NOT to choose the best document or vote among them, but to synthesize a new, superior document that incorporates the strongest elements from each.</instruction>
    <instruction>Carefully review all provided specs, identifying unique logic, validation steps, and architectural patterns that would add value to a comprehensive specification.</instruction>
    <instruction>Create a coherent, well-structured document that integrates the best parts from each spec while maintaining a consistent, technical voice and approach.</instruction>
    <instruction>Pay particular attention to areas where the specs differ, and use your expertise to determine which approach best serves the implementation requirements.</instruction>
    <instruction>Include all required sections: Overview, Key Features, Project Structure, Implementation Notes, CLI Details, Behavior Rules, Tool or Function Implementation, Testing Requirements, README Documentation, Relevant Files, and Validation.</instruction>
    <instruction>Your final document should be in professional markdown format, with clear structure including headings, bullet points, tables, and other formatting that enhances readability.</instruction>
    <instruction>Begin with an executive summary that concisely outlines the implementation strategy and key recommendations.</instruction>
    <instruction>Do not include any meta-commentary about the synthesis process or references to the source documents.</instruction>
    <instruction>The final document should read as if it were written by a single, world-class spec author with deep expertise in technical documentation.</instruction>
</instructions>

<original-requirements>{original_prompt}</original-requirements>

<spec-documents>
{team_responses}
</spec-documents>
```

### Implementation Logic

1. **Leveraging Base Persona Function**:
   - Uses the same persona_base function as other personas
   - Maintains consistent parameter handling and validation
   - Uses centralized model configuration
   - Maintains the same single-model and decision maker workflows as other personas

2. **Single Model Flow** (when `use_decision_maker` is False):
   - If no model specified, uses DEFAULT_MODEL
   - Reads prompt from file
   - Formats with Spec Author persona template
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

Register the Spec Writer tool in server.py:

```python
@mcp.tool()
def persona_sw_tool(
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    use_decision_maker: bool = False,
    decision_maker_models: List[str] = None,
    sw_prompt: str = DEFAULT_SW_PROMPT,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
    """
    Generate specification documents using a specialized Spec Author persona, with optional decision making.
    
    This tool uses a specialized Spec Author prompt to create comprehensive specification documents
    from a file. It can either use a single model or leverage the team decision-making
    functionality to get multiple perspectives and consolidate them.
    
    Args:
        from_file: Path to the file containing the requirements or PRD
        models_prefixed_by_provider: List of models in format "provider:model"
                                    (if None, defaults to DEFAULT_MODEL)
        output_dir: Directory where response files should be saved (defaults to input file's directory/responses)
        output_extension: File extension for output files (e.g., 'py', 'txt', 'md')
        output_path: Optional full output path with filename for the output document
        use_decision_maker: Whether to use the decision maker functionality
        decision_maker_models: Models to use if use_decision_maker is True
                             (if None, defaults to DEFAULT_TEAM_MODELS)
        sw_prompt: Custom spec author prompt template
        decision_maker_model: Model to use for decision making (defaults to DEFAULT_DECISION_MAKER_MODEL)
        decision_maker_prompt: Custom persona prompt template for decision making
    
    Returns:
        Path to the specification output file
    """
    return persona_sw(
        from_file=from_file,
        models_prefixed_by_provider=models_prefixed_by_provider,
        output_dir=output_dir,
        output_extension=output_extension,
        output_path=output_path,
        use_decision_maker=use_decision_maker,
        decision_maker_models=decision_maker_models,
        sw_prompt=sw_prompt,
        decision_maker_model=decision_maker_model,
        decision_maker_prompt=decision_maker_prompt
    )
```

## Relevant Files

- src/agile_team/shared/config.py - Add DEFAULT_SW_PROMPT constant
- src/agile_team/server.py - Update to register the new persona_sw_tool
- src/agile_team/tools/persona_sw.py - New file with Spec Writer persona implementation
- src/agile_team/tools/prompts/sw_prompt.md - The Spec Author prompt template
- src/agile_team/tools/prompts/sw_decision_prompt.md - The Spec Author decision maker prompt template
- src/agile_team/tests/tools/test_persona_sw.py - Test cases for Spec Writer implementation

## Testing Requirements

Tests should cover:
- Spec Writer implementation with single model
- Integration with decision maker when use_decision_maker is True
- Parameter validation and error handling
- Various output path configurations
- Custom prompt template usage

## Validation

- Run tests with `uv run pytest src/agile_team/tests/tools/test_persona_sw.py`
- Verify end-to-end functionality with sample prompts
- Validate MCP tool registration with `uv run agile-team --help`
- Update README.md with documentation for the new tool

**Implementation is only complete once this validation passes.**
