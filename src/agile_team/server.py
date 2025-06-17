"""MCP Server implementation for Agile Team."""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Optional

# Import tools
from agile_team.tools.prompt import prompt
from agile_team.tools.prompt_from_file import prompt_from_file
from agile_team.tools.prompt_from_file_to_file import prompt_from_file_to_file
from agile_team.tools.list_providers import list_providers
from agile_team.tools.list_models import list_models
from agile_team.tools.persona_dm import persona_dm, DEFAULT_PERSONA_PROMPT
from agile_team.tools.persona_ba import persona_ba, DEFAULT_BA_PROMPT, DEFAULT_BA_DECISION_PROMPT
from agile_team.tools.persona_pm import persona_pm, DEFAULT_PM_PROMPT, DEFAULT_PM_DECISION_PROMPT
from agile_team.tools.persona_sw import persona_sw, DEFAULT_SW_PROMPT_CONTENT, DEFAULT_SW_DECISION_PROMPT

# Import centralized configuration
from agile_team.shared.config import DEFAULT_MODEL, DEFAULT_TEAM_MODELS, DEFAULT_DECISION_MAKER_MODEL, DEFAULT_SW_PROMPT

# Default model for prompt tools (maintained for backward compatibility)
DEFAULT_PROMPT_MODEL = [DEFAULT_MODEL]

# Create a FastMCP server instance
mcp = FastMCP("Agile Team MCP Server")

# Register tools using decorators
@mcp.tool()
def prompt_tool(text: str, models_prefixed_by_provider: List[str] = None) -> List[str]:
    """
    Send a text prompt to multiple LLM models and return their responses.
    
    Args:
        text: The prompt text to send to the models
        models_prefixed_by_provider: List of models in format "provider:model" (e.g., "openai:gpt-4").
                                     If None, defaults to ["openai:gpt-4o-mini"]
    
    Returns:
        List of responses, one from each specified model
    """
    if models_prefixed_by_provider is None:
        models_prefixed_by_provider = DEFAULT_PROMPT_MODEL
    return prompt(text, models_prefixed_by_provider)


@mcp.tool()
def prompt_from_file_tool(file_path: str, models_prefixed_by_provider: List[str] = None) -> List[str]:
    """
    Read a prompt from a file and send it to multiple LLM models.
    
    Args:
        file_path: Path to the file containing the prompt text
        models_prefixed_by_provider: List of models in format "provider:model" (e.g., "openai:gpt-4").
                                     If None, defaults to ["openai:gpt-4o-mini"]
    
    Returns:
        List of responses, one from each specified model
    """
    if models_prefixed_by_provider is None:
        models_prefixed_by_provider = DEFAULT_PROMPT_MODEL
    return prompt_from_file(file_path, models_prefixed_by_provider)


@mcp.tool()
def prompt_from_file2file_tool(
    file_path: str, models_prefixed_by_provider: List[str] = None, output_dir: str = None, 
    output_extension: str = None, output_path: str = None
) -> List[str]:
    """
    Read a prompt from a file, send it to multiple LLM models, and write responses to files.
    
    Args:
        file_path: Path to the file containing the prompt text
        models_prefixed_by_provider: List of models in format "provider:model" (e.g., "openai:gpt-4").
                                     If None, defaults to ["openai:gpt-4o-mini"]
        output_dir: Directory where response files should be saved (defaults to input file's directory/responses)
        output_extension: File extension for output files (e.g., 'py', 'txt', 'md')
                          If None, defaults to 'md' (default: None)
        output_path: Optional full output path with filename. If provided, the extension
                     from this path will be used (overrides output_extension).
    
    Returns:
        List of file paths where responses were written
    """
    if models_prefixed_by_provider is None:
        models_prefixed_by_provider = DEFAULT_PROMPT_MODEL
    return prompt_from_file_to_file(file_path, models_prefixed_by_provider, output_dir, output_extension, output_path)


@mcp.tool()
def list_providers_tool() -> Dict[str, List[str]]:
    """
    List all supported LLM providers.

    Returns:
        Dictionary with main providers and their shortcuts clearly formatted
    """
    return list_providers()


@mcp.tool()
def list_models_tool(provider: str) -> List[str]:
    """
    List all available models for a specific provider.
    
    Args:
        provider: The provider to list models for (e.g., "openai", "anthropic")
    
    Returns:
        List of model names available for the specified provider
    """
    return list_models(provider)


@mcp.tool()
def persona_dm_tool(
    from_file: str,
    models_prefixed_by_provider: Optional[List[str]] = None,
    output_dir: Optional[str] = None,
    output_extension: Optional[str] = None,
    output_path: Optional[str] = None,
    persona_dm_model: str = DEFAULT_DECISION_MAKER_MODEL, 
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
        persona_dm_model: Model to use for making the decision (defaults to DEFAULT_DECISION_MAKER_MODEL)
        persona_prompt: Custom persona prompt template (if None, uses the default)
    
    Returns:
        Path to the persona output file
    """
    return persona_dm(
        from_file=from_file,
        models_prefixed_by_provider=models_prefixed_by_provider,
        output_dir=output_dir,
        output_extension=output_extension,
        output_path=output_path,
        persona_dm_model=persona_dm_model,
        persona_prompt=persona_prompt
    )


@mcp.tool()
def persona_ba_tool(
    from_file: str,
    models_prefixed_by_provider: Optional[List[str]] = None,
    output_dir: Optional[str] = None,
    output_extension: Optional[str] = None,
    output_path: Optional[str] = None,
    use_decision_maker: bool = False,
    decision_maker_models: Optional[List[str]] = None,
    ba_prompt: str = DEFAULT_BA_PROMPT,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_BA_DECISION_PROMPT
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


@mcp.tool()
def persona_pm_tool(
    from_file: str,
    models_prefixed_by_provider: Optional[List[str]] = None,
    output_dir: Optional[str] = None,
    output_extension: Optional[str] = None,
    output_path: Optional[str] = None,
    use_decision_maker: bool = False,
    decision_maker_models: Optional[List[str]] = None,
    pm_prompt: str = DEFAULT_PM_PROMPT,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_PM_DECISION_PROMPT
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


@mcp.tool()
def persona_sw_tool(
    from_file: str,
    models_prefixed_by_provider: Optional[List[str]] = None,
    output_dir: Optional[str] = None,
    output_extension: Optional[str] = None,
    output_path: Optional[str] = None,
    use_decision_maker: bool = False,
    decision_maker_models: Optional[List[str]] = None,
    sw_prompt: str = DEFAULT_SW_PROMPT_CONTENT,
    decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL,
    decision_maker_prompt: str = DEFAULT_SW_DECISION_PROMPT
) -> str:
    """
    Generate specification documents using a specialized Spec Writer persona, with optional decision making.
    
    This tool uses a specialized Spec Writer prompt to create comprehensive specification documents
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
        sw_prompt: Custom spec writer prompt template
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


@mcp.prompt()
def list_mcp_assets() -> str:
    """
    List MCP Assets prompt for comprehensive server capability overview.

    Provides dynamic listing of all available prompts, tools, and resources
    with usage examples and quick start guidance.
    """
    
    content = """# 🚀 Agile Team MCP Server Assets

## 📝 Prompts
Interactive conversation starters and guided workflows:

• **list_mcp_assets** () - Comprehensive overview of all server capabilities

## 🔧 Tools
Agent persona management and LLM provider integration functions:

### Core Prompt Tools
• **prompt_tool** (text, models_prefixed_by_provider) - Send text prompts to multiple LLM models
• **prompt_from_file_tool** (file_path, models_prefixed_by_provider) - Send prompts from files to models
• **prompt_from_file2file_tool** (file_path, models_prefixed_by_provider, output_dir, output_extension, output_path) - Process prompts from files and save responses

### Provider Discovery
• **list_providers_tool** () - List all supported LLM providers with shortcuts
• **list_models_tool** (provider) - List available models for a specific provider

### Agent Personas
• **persona_ba_tool** (from_file, models_prefixed_by_provider, use_decision_maker, ...) - Business Analyst persona for project briefs and requirements
• **persona_pm_tool** (from_file, models_prefixed_by_provider, use_decision_maker, ...) - Product Manager persona for PRDs and product plans
• **persona_sw_tool** (from_file, models_prefixed_by_provider, use_decision_maker, ...) - Spec Writer persona for technical specifications
• **persona_dm_tool** (from_file, models_prefixed_by_provider, persona_dm_model, ...) - Team Decision Maker for multi-model consensus

---

## 🏢 Supported LLM Providers

| Provider | Short Prefix | Full Prefix | Example Usage |
|----------|--------------|-------------|--------------|
| OpenAI   | `o`          | `openai`    | `o:gpt-4o-mini` |
| Anthropic | `a`         | `anthropic` | `a:claude-3-5-haiku` |
| Google Gemini | `g`     | `gemini`    | `g:gemini-2.5-pro-exp` |
| Groq     | `q`          | `groq`      | `q:llama-3.1-70b-versatile` |
| DeepSeek | `d`          | `deepseek`  | `d:deepseek-coder` |
| Ollama   | `l`          | `ollama`    | `l:llama3.1` |

---

## 🎯 Quick Start Agile Team Workflow

### Business Analysis → Product Management → Specification

1. **Analyze Business Requirements**
   ```
   Use tool: persona_ba_tool
   Arguments: from_file="requirements/concept.md"
   Result: Comprehensive project brief with MVP scope and business analysis
   ```

2. **Create Product Plan**
   ```
   Use tool: persona_pm_tool
   Arguments: from_file="responses/project-brief.md"
   Result: Detailed PRD with features, timelines, and success metrics
   ```

3. **Generate Technical Specification**
   ```
   Use tool: persona_sw_tool
   Arguments: from_file="responses/project-prd.md"
   Result: Developer-ready specification with implementation details
   ```

4. **Team Decision Making**
   ```
   Use tool: persona_dm_tool
   Arguments: from_file="requirements/decision.md", models_prefixed_by_provider=["o:gpt-4.1", "a:claude-3-7-sonnet", "g:gemini-2.5-pro"]
   Result: Multi-model analysis with final decision and reasoning
   ```

---

## 🔄 Advanced Workflows

### Multi-Model Analysis Pattern
Send the same prompt to multiple models for comparison:
```bash
# Compare responses across providers
prompt_tool: "Analyze the trade-offs between microservices and monoliths" ["o:gpt-4.1", "a:claude-3-7-sonnet", "g:gemini-2.5-pro"]
```

### Team-Based Persona Decision Making
Enable team decision making for any persona:
```bash
# Business Analysis with team consensus
persona_ba_tool: "requirements.md" use_decision_maker=true decision_maker_models=["o:gpt-4.1", "a:claude-3-7-sonnet", "g:gemini-2.5-pro"]
```

### File-to-File Processing
Process prompts from files and automatically save responses:
```bash
# Batch process multiple prompts
prompt_from_file2file_tool: "prompts/architecture.md" ["a:claude-3-7-sonnet"] output_extension="md"
```

---

## 💡 Pro Tips

### Model Selection Strategy
• **Quick Iterations**: Use `o:gpt-4o-mini` or `a:claude-3-5-haiku` for fast responses
• **Deep Analysis**: Use `o:gpt-4.1`, `a:claude-3-7-sonnet`, or `g:gemini-2.5-pro` for comprehensive work
• **Reasoning Tasks**: Add `:high` to OpenAI models (e.g., `o:gpt-4.1:high`) for enhanced reasoning
• **Thinking Tokens**: Add `:4k` for extended thinking (e.g., `a:claude-3-7-sonnet:4k`)

### Persona Workflow Optimization
• **Start with BA**: Always begin with Business Analyst for clear requirements
• **PM for Structure**: Use Product Manager to organize features and priorities
• **SW for Implementation**: Spec Writer provides developer-ready technical details
• **DM for Consensus**: Decision Maker synthesizes multiple expert perspectives

### File Organization
• **Input Structure**: Place requirements in `prompts/` or dedicated directories
• **Output Management**: Responses automatically organized in `responses/` subdirectories
• **Traceability**: Maintain clear file naming for workflow continuity

### Best Practices
• **Phase-Based Development**: Follow BA → PM → SW → Implementation pipeline
• **Multi-Model Validation**: Use team decision making for critical decisions
• **Provider Diversity**: Leverage different models' strengths for specialized tasks
• **Version Control**: Track iterations of requirements, PRDs, and specifications

---

## 📊 Persona Capabilities

### Business Analyst
• **Project Briefs**: Transform concepts into structured business requirements
• **MVP Definition**: Define minimum viable product scope and features
• **Market Analysis**: Analyze target users and business opportunities
• **Risk Assessment**: Identify constraints, assumptions, and potential blockers

### Product Manager
• **PRD Creation**: Develop comprehensive Product Requirements Documents
• **Feature Prioritization**: Organize features by business value and impact
• **Success Metrics**: Define measurable outcomes and KPIs
• **Technical Handoff**: Prepare requirements for development teams

### Spec Writer
• **Technical Specifications**: Create developer-ready implementation guides
• **Architecture Patterns**: Define system structure and component interactions
• **Validation Criteria**: Establish testing and acceptance requirements
• **Implementation Steps**: Provide detailed development instructions

### Decision Maker
• **Multi-Model Analysis**: Synthesize insights from multiple AI perspectives
• **Consensus Building**: Evaluate different approaches and choose optimal solutions
• **Risk Assessment**: Analyze trade-offs across multiple dimensions
• **Rationale Documentation**: Provide clear reasoning for decisions

---

**🚀 Ready to build your next project? Start with `persona_ba_tool` to analyze your business requirements!**"""

    return content