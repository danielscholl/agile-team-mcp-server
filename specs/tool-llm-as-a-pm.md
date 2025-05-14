# Feature: LLM as a Product Manager (Persona PM)

> A tool for performing tasks typically handled by a Product Manager, with optional decision-making integration.

## Implementation Details

The persona_pm tool provides a specialized product management framework using a Product Manager persona, built on the reusable persona architecture:

- Leverages the same base persona function used by other personas
- Uses a specialized Product Manager prompt template to create product plans
- Integrates with the persona_dm tool for team-based decision making
- Returns detailed product plans formatted in markdown
- Prompts exist outside of the {tool}.py and are maintained in tools/prompts

### Core Function Signatures

#### Product Manager Persona

```python
def persona_pm(
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    use_decision_maker: bool = False,
    decision_maker_models: List[str] = None,
    pm_prompt: str = DEFAULT_PM_PROMPT,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
    """
    Product Manager persona implementation.
    """
    return persona_base(
        persona_name="product_manager",
        persona_prompt=pm_prompt,
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

### Product Manager Prompt Template

```xml
<purpose>
    You are a world-class expert Product Manager with deep expertise in product development, roadmap planning, and feature prioritization. 
    You excel at translating business requirements into technical specifications and creating detailed product plans with clear milestones and deliverables.
</purpose>

<capabilities>
    <capability>Product vision and strategy development</capability>
    <capability>Feature prioritization and roadmap planning</capability>
    <capability>Market and competitive analysis</capability>
    <capability>User story and requirements definition</capability>
    <capability>Cross-functional team collaboration</capability>
    <capability>Data-driven decision making</capability>
</capabilities>

<modes>   
    <mode>
        <n>Product Planning Mode</n>
        <description>Create comprehensive product plans with prioritized features and clear timelines</description>
        <outputs>
            <o>Product Vision</o>
            <o>Target Market/User Personas</o>
            <o>Feature List (Prioritized)</o>
            <o>Development Roadmap</o>
            <o>Success Metrics</o>
            <o>Risk Assessment</o>
        </outputs>
        <tone>Strategic, methodical, user-focused, data-oriented</tone>
    </mode>
</modes>

<instructions>
    <instruction>Identify the product needs based on the user's request. If unclear, assume Product Planning Mode.</instruction>
    <instruction>For Product Planning Mode: Develop a comprehensive product plan with prioritized features and clear timelines.</instruction>
    <instruction>Use structured formats (lists, tables, sections) for outputs and avoid ambiguity.</instruction>
    <instruction>Ensure your product plan is well-structured, clear, and actionable.</instruction>
    <instruction>Prioritize understanding user needs and market opportunities.</instruction>
    <instruction>Be capable of explaining product management concepts or methodologies clearly if requested.</instruction>
    <instruction>Create a product plan that is well-structured, just like a real product manager would.</instruction>
    <instruction>Do not include any metadata, headers, footers, or formatting that isn't part of the actual product plan.</instruction>
    <instruction>Do not ask additional questions, just provide the requested output.</instruction>
</instructions>

<interaction-flow>
    <step>Identify Product Needs: Determine the product requirements and objectives</step>
    <step>Market Analysis: Assess market opportunity and competitive landscape</step>
    <step>Feature Planning: Define and prioritize product features</step>
    <step>Roadmap Development: Create timeline with milestones and deliverables</step>
    <step>Output Generation: Structure plan into appropriate format</step>
    <step>Presentation: Present final product plan document</step>
</interaction-flow>

<pm-request>{pm_request}</pm-request>
```

### Product Manager Decision Maker Prompt Template

```xml
<purpose>
    You are a master Product Management synthesizer. You have received multiple product plans from different AI models. Your job is to craft the perfect, comprehensive product plan by extracting and combining the best insights and approaches from all submitted plans.
</purpose>
<instructions>
    <instruction>You have been provided with the original product requirements and multiple AI-generated product plans.</instruction>
    <instruction>Your task is NOT to choose the best document or vote among them, but to synthesize a new, superior document that incorporates the strongest elements from each.</instruction>
    <instruction>Carefully review all provided plans, identifying unique insights, methodologies, and frameworks that would add value to a comprehensive product strategy.</instruction>
    <instruction>Create a coherent, well-structured document that integrates the best parts from each plan while maintaining a consistent voice and approach.</instruction>
    <instruction>Pay particular attention to areas where the plans differ, and use your expertise to determine which approach best serves the product requirements.</instruction>
    <instruction>Include comprehensive sections on: product vision, target market, feature prioritization, development roadmap, success metrics, risk assessment, and any other relevant areas.</instruction>
    <instruction>Your final document should be in professional markdown format, with clear structure including headings, bullet points, tables, and other formatting that enhances readability.</instruction>
    <instruction>Begin with an executive summary that concisely outlines the product strategy and key recommendations.</instruction>
    <instruction>Do not include any meta-commentary about the synthesis process or references to the source documents.</instruction>
    <instruction>The final document should read as if it were written by a single, world-class product manager with deep expertise in the domain.</instruction>
</instructions>

<original-requirements>{original_prompt}</original-requirements>

<product-plans>
{team_responses}
</product-plans>
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
   - Formats with PM persona template
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

Register the Product Manager tool in server.py:

```python
@mcp.tool()
def persona_pm_tool(
    from_file: str,
    models_prefixed_by_provider: List[str] = None,
    output_dir: str = None,
    output_extension: str = None,
    output_path: str = None,
    use_decision_maker: bool = False,
    decision_maker_models: List[str] = None,
    pm_prompt: str = DEFAULT_PM_PROMPT,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_PERSONA_PROMPT
) -> str:
    """
    Generate product management plans using a specialized Product Manager persona, with optional decision making.
    
    This tool uses a specialized Product Manager prompt to create comprehensive product plans
    from a file. It can either use a single model or leverage the team decision-making
    functionality to get multiple perspectives and consolidate them.
    
    Args:
        from_file: Path to the file containing the product requirements
        models_prefixed_by_provider: List of models in format "provider:model"
                                    (if None, defaults to DEFAULT_MODEL)
        output_dir: Directory where response files should be saved (defaults to input file's directory/responses)
        output_extension: File extension for output files (e.g., 'py', 'txt', 'md')
        output_path: Optional full output path with filename for the output document
        use_decision_maker: Whether to use the decision maker functionality
        decision_maker_models: Models to use if use_decision_maker is True
                             (if None, defaults to DEFAULT_TEAM_MODELS)
        pm_prompt: Custom product manager prompt template
        decision_maker_model: Model to use for decision making (defaults to DEFAULT_DECISION_MAKER_MODEL)
        decision_maker_prompt: Custom persona prompt template for decision making
    
    Returns:
        Path to the product plan output file
    """
    return persona_pm(
        from_file=from_file,
        models_prefixed_by_provider=models_prefixed_by_provider,
        output_dir=output_dir,
        output_extension=output_extension,
        output_path=output_path,
        use_decision_maker=use_decision_maker,
        decision_maker_models=decision_maker_models,
        pm_prompt=pm_prompt,
        decision_maker_model=decision_maker_model,
        decision_maker_prompt=decision_maker_prompt
    )
```

## Relevant Files

- src/agile_team/shared/config.py - Add DEFAULT_PM_PROMPT constant
- src/agile_team/server.py - Update to register the new persona_pm_tool
- src/agile_team/tools/persona_pm.py - New file with Product Manager persona implementation
- src/agile_team/tools/prompts/pm_prompt.md - The Product Manager prompt template
- src/agile_team/tools/prompts/pm_decision_prompt.md - The Product Manager decision maker prompt template
- src/agile_team/tests/tools/test_persona_pm.py - Test cases for PM implementation

## Testing Requirements

Tests should cover:
- Product Manager implementation with single model
- Integration with decision maker when use_decision_maker is True
- Parameter validation and error handling
- Various output path configurations
- Custom prompt template usage

## Validation

- Run tests with `uv run pytest src/agile_team/tests/tools/test_persona_pm.py`
- Verify end-to-end functionality with sample prompts
- Validate MCP tool registration with `uv run agile-team --help`
- Update README.md with documentation for the new tool