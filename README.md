# Agile Team MCP Server

A team of Agent Personas wrapped in an MCP server that has the ability to leverage at scale massive compute by wrapping various LLM providers to perform activities as an Agile Team Persona.

## Features

- **Model Wrapping**: Send prompts to multiple LLM models with a unified interface
- **Provider/Model Correction**: Automatically correct and validate provider and model names
- **File Support**: Send prompts from files and save responses to files
- **Provider/Model Discovery**: List available providers and models
- **Persona Tools**: Specialized personas like Business Analyst, Product Manager, Spec Writer, and Team Decision Maker

## Setup

### Installation

```bash
# Clone and install
git clone https://github.com/danielscholl/agile-team-mcp-server.git
cd agile-team-mcp-server
uv sync

# Install
uv pip install -e .

# Run tests to verify installation
uv run pytest
```

### Environment Configuration

Create and edit your `.env` file with your API keys:

```bash
# Create environment file from template
cp .env.sample .env
```

Required API keys in your `.env` file:
```
# Required API keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here  # For Google Gemini models
GROQ_API_KEY=your_groq_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OLLAMA_HOST=http://localhost:11434

# Optional model configuration
DEFAULT_MODEL=openai:gpt-4o-mini
DEFAULT_TEAM_MODELS=["openai:gpt-4.1","anthropic:claude-3-7-sonnet","gemini:gemini-2.5-pro"]
DEFAULT_DECISION_MAKER_MODEL=openai:gpt-4o-mini
```

## MCP Server Configuration

To utilize this MCP server directly in other projects either use the buttons to install in VSCode, edit the `.mcp.json` file directory.

> Clients tend to have slighty different configurations

[![Install with UV in VS Code](https://img.shields.io/badge/VS_Code-UV-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect?url=vscode:mcp/install?%7B%22name%22%3A%22agile-team%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fdanielscholl%2Fagile-team-mcp-server%40main%22%2C%22agile-team%22%5D%2C%22env%22%3A%7B%22OPENAI_API_KEY%22%3A%22%24%7Binput%3Aopenai_key%7D%22%2C%22ANTHROPIC_API_KEY%22%3A%22%24%7Binput%3Aanthropic_key%7D%22%2C%22GOOGLE_API_KEY%22%3A%22%24%7Binput%3Agemini_key%7D%22%2C%22GROQ_API_KEY%22%3A%22%24%7Binput%3Agroq_key%7D%22%2C%22DEEPSEEK_API_KEY%22%3A%22%24%7Binput%3Adeepseek_key%7D%22%2C%22OLLAMA_HOST%22%3A%22http%3A%2F%2Flocalhost%3A11434%22%2C%22DEFAULT_MODEL%22%3A%22openai%3Agpt-4o-mini%22%2C%22DEFAULT_TEAM_MODELS%22%3A%22%5B%5C%22openai%3Agpt-4.1%5C%22%2C%5C%22anthropic%3Aclaude-3-7-sonnet%5C%22%2C%5C%22gemini%3Agemini-2.5-pro%5C%22%5D%22%2C%22DEFAULT_DECISION_MAKER_MODEL%22%3A%22openai%3Agpt-4o-mini%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22openai_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22OpenAI%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22anthropic_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Anthropic%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22gemini_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Google%20Gemini%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22groq_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Groq%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22deepseek_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22DeepSeek%20API%20Key%22%2C%22password%22%3Atrue%7D%5D%7D)   [![Install with Docker in VS Code](https://img.shields.io/badge/VS_Code-Docker-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect?url=vscode:mcp/install?%7B%22name%22%3A%22agile-team%22%2C%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22--mount%22%2C%22type%3Dbind%2Csource%3D%3CYOUR_WORKSPACE_PATH%3E%2Ctarget%3D%2Fworkspace%22%2C%22danielscholl%2Fagile-team-mcp-server%22%5D%2C%22env%22%3A%7B%22OPENAI_API_KEY%22%3A%22%24%7Binput%3Aopenai_key%7D%22%2C%22ANTHROPIC_API_KEY%22%3A%22%24%7Binput%3Aanthropic_key%7D%22%2C%22GOOGLE_API_KEY%22%3A%22%24%7Binput%3Agemini_key%7D%22%2C%22GROQ_API_KEY%22%3A%22%24%7Binput%3Agroq_key%7D%22%2C%22DEEPSEEK_API_KEY%22%3A%22%24%7Binput%3Adeepseek_key%7D%22%2C%22OLLAMA_HOST%22%3A%22http%3A%2F%2Flocalhost%3A11434%22%2C%22DEFAULT_MODEL%22%3A%22openai%3Agpt-4o-mini%22%2C%22DEFAULT_TEAM_MODELS%22%3A%22%5B%5C%22openai%3Agpt-4.1%5C%22%2C%5C%22anthropic%3Aclaude-3-7-sonnet%5C%22%2C%5C%22gemini%3Agemini-2.5-pro%5C%22%5D%22%2C%22DEFAULT_DECISION_MAKER_MODEL%22%3A%22openai%3Agpt-4o-mini%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22openai_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22OpenAI%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22anthropic_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Anthropic%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22gemini_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Google%20Gemini%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22groq_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Groq%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22deepseek_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22DeepSeek%20API%20Key%22%2C%22password%22%3Atrue%7D%5D%7D)

### Configure for Claude.app

```json
{
  "mcpServers": {
    "agile-team": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/danielscholl/agile-team-mcp-server@main",
        "agile-team"
      ],
      "env": {
        "OPENAI_API_KEY": "<YOUR_OPENAI_KEY>",
        "ANTHROPIC_API_KEY": "<YOUR_ANTHROPIC_KEY>",
        "GEMINI_API_KEY": "<YOUR_GEMINI_KEY>",
        "GROQ_API_KEY": "<YOUR_GROQ_KEY>",
        "DEEPSEEK_API_KEY": "<YOUR_DEEPSEEK_KEY>",
        "OLLAMA_HOST": "http://localhost:11434",
        "DEFAULT_MODEL": "openai:gpt-4o-mini",
        "DEFAULT_TEAM_MODELS": "[\"openai:gpt-4.1\",\"anthropic:claude-3-7-sonnet\",\"gemini:gemini-2.5-pro\"]",
        "DEFAULT_DECISION_MAKER_MODEL": "openai:gpt-4o-mini"
      }
    }
  }
}
```

### Configure for Claude.code

Setting up Agile Team with Claude Code easily by importing it.

```bash
claude mcp add-from-claude-desktop
```

> Note: "--directory" would be the path to the source code if not in the same directory.

```bash
# Copy this JSON configuration
{
    "command": "uvx",
    "args": ["--from", "git+https://github.com/danielscholl/agile-team-mcp-server@main", "agile-team"],
    "env": {
        "DEFAULT_MODEL": "openai:gpt-4o-mini",
        "DEFAULT_TEAM_MODELS": "[\"openai:gpt-4.1\",\"anthropic:claude-3-7-sonnet\",\"gemini:gemini-2.5-pro\"]",
        "DEFAULT_DECISION_MAKER_MODEL": "openai:gpt-4o-mini"
    }
}

# Then run this command in Claude Code
claude mcp add agile-team "$(pbpaste)"
```

To remove the configuration later:
```bash
claude mcp remove agile-team
```

## Available LLM Providers

| Provider | Short Prefix | Full Prefix | Example Usage |
|----------|--------------|-------------|--------------|
| OpenAI   | `o`          | `openai`    | `o:gpt-4o-mini` |
| Anthropic | `a`         | `anthropic` | `a:claude-3-5-haiku` |
| Google Gemini | `g`     | `gemini`    | `g:gemini-2.5-pro-exp-03-25` |
| Groq     | `q`          | `groq`      | `q:llama-3.1-70b-versatile` |
| DeepSeek | `d`          | `deepseek`  | `d:deepseek-coder` |
| Ollama   | `l`          | `ollama`    | `l:llama3.1` |


## Usage

### Command Line

Run the server directly:

```bash
uv run agile-team
```

### With MCP Client

With a compatible MCP client, you can connect to the server:

```bash
mcp use agile-team
```

## Available Prompts

Interactive conversation starters and guided workflows to help you discover and use server capabilities.

### List MCP Assets

Get a comprehensive overview of all server capabilities including tools, personas, providers, and workflows.

**Parameters**: None required

**Usage**:
```bash
# Get complete server capability overview
list_mcp_assets
```

**Returns**: Comprehensive markdown documentation including:
- All available tools with parameters and examples
- Supported LLM providers with shortcuts and usage examples  
- Agent personas (Business Analyst, Product Manager, Spec Writer, Decision Maker)
- Quick start workflows for agile team processes
- Advanced usage patterns and best practices
- Pro tips for model selection and workflow optimization

This prompt provides a self-documenting overview of the entire agile-team MCP server, making it easy to discover capabilities and get started with productive workflows.

## Available Tools

### List Available Options

Tools to discover available LLM providers and their supported models.

#### List Providers Tool

Lists all supported LLM providers and their shortcut prefixes.

**Parameters**: None required

**Examples**:
```bash
# Simple example
list_providers_tool
```

#### List Models Tool

Lists all available models for a specific provider.

**Parameters**:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `provider` | The provider to list models for (e.g., "openai", "anthropic") | *required* |

**Examples**:
```bash
# Simple example with full provider name
list_models_tool: "openai"

# Using provider shortcode
list_models_tool: "a"  # Lists Anthropic models
```

### Send Prompts to Models

Send text prompts directly to LLM models and get their responses.

**Parameters**:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `text` | The prompt text to send to the models | *required* |
| `models_prefixed_by_provider` | List of models in format "provider:model" | `openai:gpt-4o-mini` |

**Features**:
- Send prompts to one or multiple models simultaneously
- Use model suffixes for special behaviors:
  - `:4k` or other numbers for thinking token budgets
  - `:high` for increased reasoning effort (OpenAI only)

**Examples**:
```bash
# Simple example
prompt_tool: "Create a plan for implementing user authentication"

# Complex example with multiple models and options
prompt_tool: "Analyze the trade-offs between microservices and monoliths" ["openai:gpt-4.1:high", "anthropic:claude-3-7-sonnet:4k"]
```

### Work with Files

Process prompts from files and save responses to files for batch processing.

#### From File Tool

**Parameters**:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `file_path` | Path to the file containing the prompt | *required* |
| `models_prefixed_by_provider` | List of models in format "provider:model" | `openai:gpt-4o-mini` |

**Examples**:
```bash
# Simple example
prompt_from_file_tool: "prompts/function.md"

# Complex example with specific model
prompt_from_file_tool: "prompts/function.md" ["anthropic:claude-3-7-sonnet-20250219"]
```

#### From File to File Tool

**Parameters**:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `file_path` | Path to the file containing the prompt | *required* |
| `models_prefixed_by_provider` | List of models in format "provider:model" | `openai:gpt-4o-mini` |
| `output_path` | Full path for the output file | Generated based on input |
| `output_dir` | Directory for response files | input file's directory/responses |
| `output_extension` | File extension for output files | `md` |

**Examples**:
```bash
# Simple example
prompt_from_file2file_tool: "prompts/uv_script.md"

# Complex example with specific model, output path and custom extension
prompt_from_file2file_tool: "prompts/diagram.md" ["anthropic:claude-3-7-sonnet"] "prompts/responses/architecture_diagram.md"
```

### Team Decision Making

Use multiple models as team members to generate different solutions, then have a decision maker model evaluate and choose the best approach.

**Parameters**:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `from_file` | Path to the file containing the prompt | *required* |
| `models_prefixed_by_provider` | List of team member models | `["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"]` |
| `persona_dm_model` | Model for making the decision | `openai:gpt-4o-mini` |
| `output_path` | Full path for the output document | Generated based on input |
| `output_dir` | Directory for response files | input file's directory/responses |
| `output_extension` | File extension for output files | `md` |
| `persona_prompt` | Custom decision maker prompt | Default template |

**Examples**:
```bash
# Simple example
persona_dm_tool: "prompts/decision.md"

# Complex example with custom team and decision maker model
persona_dm_tool: "prompts/decision.md" ["o:gpt-4.1", "a:claude-3-7-sonnet", "g:gemini-2.5-pro-preview-03-25"] persona_dm_model="o:o3" "prompts/responses/final_decision.md"
```

### Business Analyst Persona

Generate detailed business analysis using a specialized Business Analyst persona, with optional team-based decision making.

**Capabilities**:
- Creating detailed project briefs and requirement documents
- Analyzing business needs and market opportunities
- Defining MVP scope and feature prioritization
- Identifying target audiences and user personas

**Parameters**:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `from_file` | Path to the file containing business requirements | *required* |
| `models_prefixed_by_provider` | Models to use in format "provider:model" | `openai:gpt-4o-mini` |
| `output_path` | Full path for the output document | Generated based on input |
| `output_dir` | Directory for response files | input file's directory/responses |
| `output_extension` | File extension for output files | `md` |
| `use_decision_maker` | Whether to use team decision making | `false` |
| `decision_maker_models` | Models for team members if using decision maker | `["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"]` |
| `decision_maker_model` | Model for final decision making | `openai:gpt-4o-mini` |

**Examples**:
```bash
# Simple example
persona_ba_tool: "prompts/concept.md" "prompts/responses/project-brief.md"

# Complex example with team-based decision making
persona_ba_tool: "prompts/concept.md" use_decision_maker=true decision_maker_model="o:04-mini" "prompts/responses/project-brief.md"
```

### Product Manager Persona

Generate comprehensive product management plans using a specialized Product Manager persona, with optional team-based decision making.

**Capabilities**:
- Creating detailed product plans with prioritized features and clear timelines
- Developing product vision and strategy
- Performing market and competitive analysis
- Defining user stories and requirements
- Managing cross-functional team collaboration
- Implementing data-driven decision making

**Parameters**:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `from_file` | Path to the file containing the product requirements | *required* |
| `models_prefixed_by_provider` | Models to use in format "provider:model" | `openai:gpt-4o-mini` |
| `output_path` | Full path for the output document | Generated based on input |
| `output_dir` | Directory for response files | input file's directory/responses |
| `output_extension` | File extension for output files | `md` |
| `use_decision_maker` | Whether to use team decision making | `false` |
| `decision_maker_models` | Models for team members if using decision maker | `["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"]` |
| `decision_maker_model` | Model for final decision making | `openai:gpt-4o-mini` |
| `pm_prompt` | Custom Product Manager prompt template | Default template |
| `decision_maker_prompt` | Custom decision maker prompt template | Default template |

**Examples**:
```bash
# Simple example
persona_pm_tool: "prompts/responses/project-brief.md" "prompts/responses/project-prd.md"

# Complex example with team-based decision making
persona_pm_tool: "prompts/responses/project-brief.md" use_decision_maker=true decision_maker_model="o:gpt-4o-mini" "prompts/responses/project-prd.md"
```

### Spec Writer Persona

Generate clear, developer-ready specification documents from PRDs, project briefs, or user requests using a specialized Spec Writer persona.

**Capabilities**:
- Producing technical specifications from PRDs or project briefs
- Defining step-by-step implementation instructions for developers and AI agents
- Creating comprehensive specifications with architectural patterns and validation criteria
- Defining tool behavior, CLI structure, directory layout, and testing plans
- Using focused, reproducible examples to communicate architectural patterns
- Ensuring each spec includes validation steps to verify implementation

**Parameters**:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `from_file` | Path to the file containing requirements or PRD | *required* |
| `models_prefixed_by_provider` | Models to use in format "provider:model" | `openai:gpt-4o-mini` |
| `output_path` | Full path for the output document | Generated based on input |
| `output_dir` | Directory for response files | input file's directory/responses |
| `output_extension` | File extension for output files | `md` |
| `use_decision_maker` | Whether to use team decision making | `false` |
| `decision_maker_models` | Models for team members if using decision maker | `["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"]` |
| `decision_maker_model` | Model for final decision making | `openai:gpt-4o-mini` |
| `sw_prompt` | Custom Spec Writer prompt template | Default template |
| `decision_maker_prompt` | Custom decision maker prompt template | Default template |

**Examples**:
```bash
# Simple example - generate a specification from a PRD
persona_sw_tool: "prompts/responses/project-prd.md" "prompts/responses/project-spec.md"

# Complex example with team-based decision making
persona_sw_tool: "prompts/responses/project-prd.md" use_decision_maker=true decision_maker_model=["o:gpt-4o-mini"] "prompts/responses/project-spec.md"
```