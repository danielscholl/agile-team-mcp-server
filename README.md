# Agile Team MCP Server

A team of Agent Personas wrapped in an MCP server that has the ability to leverage at scale massive compute by wrapping various LLM providers to perform activities as an Agile Team Persona.

## Features

- **Model Wrapping**: Send prompts to multiple LLM models with a unified interface
- **Provider/Model Correction**: Automatically correct and validate provider and model names
- **File Support**: Send prompts from files and save responses to files
- **Provider/Model Discovery**: List available providers and models

## Setup

### Installation

```bash
# Clone and install
git clone https://github.com/danielscholl/agile-team-mcp-server.git
cd just-prompt
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
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OLLAMA_HOST=http://localhost:11434
```

## MCP Server Configuration

To utilize this MCP server directly in other projects either use the buttons to install in VSCode, edit the `.mcp.json` file directory.

> Clients tend to have slighty different configurations

[![Install with UV in VS Code](https://img.shields.io/badge/VS_Code-UV-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect?url=vscode:mcp/install?%7B%22name%22%3A%22just-prompt%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fdanielscholl%2Fagile-team-mcp-server%40main%22%2C%22just-prompt%22%2C%22--default-models%22%2C%22high%2Copenai%3Ao4-mini%3Ahigh%2Canthropic%3Aclaude-3-7-sonnet-20250219%3A4k%2Cgemini%3Agemini-2.5-pro-preview-03-25%2Cgemini%3Agemini-2.5-flash-preview-04-17%22%5D%2C%22env%22%3A%7B%22OPENAI_API_KEY%22%3A%22%24%7Binput%3Aopenai_key%7D%22%2C%22ANTHROPIC_API_KEY%22%3A%22%24%7Binput%3Aanthropic_key%7D%22%2C%22GEMINI_API_KEY%22%3A%22%24%7Binput%3Agemini_key%7D%22%2C%22GROQ_API_KEY%22%3A%22%24%7Binput%3Agroq_key%7D%22%2C%22DEEPSEEK_API_KEY%22%3A%22%24%7Binput%3Adeepseek_key%7D%22%2C%22OLLAMA_HOST%22%3A%22http%3A%2F%2Flocalhost%3A11434%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22openai_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22OpenAI%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22anthropic_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Anthropic%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22gemini_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Google%20Gemini%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22groq_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Groq%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22deepseek_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22DeepSeek%20API%20Key%22%2C%22password%22%3Atrue%7D%5D%7D)   [![Install with Docker in VS Code](https://img.shields.io/badge/VS_Code-Docker-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect?url=vscode:mcp/install?%7B%22name%22%3A%22just-prompt%22%2C%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22--mount%22%2C%22type%3Dbind%2Csource%3D%3CYOUR_WORKSPACE_PATH%3E%2Ctarget%3D%2Fworkspace%22%2C%22danielscholl%2Fagile-team-mcp-server%22%5D%2C%22env%22%3A%7B%22OPENAI_API_KEY%22%3A%22%24%7Binput%3Aopenai_key%7D%22%2C%22ANTHROPIC_API_KEY%22%3A%22%24%7Binput%3Aanthropic_key%7D%22%2C%22GEMINI_API_KEY%22%3A%22%24%7Binput%3Agemini_key%7D%22%2C%22GROQ_API_KEY%22%3A%22%24%7Binput%3Agroq_key%7D%22%2C%22DEEPSEEK_API_KEY%22%3A%22%24%7Binput%3Adeepseek_key%7D%22%2C%22OLLAMA_HOST%22%3A%22http%3A%2F%2Flocalhost%3A11434%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22openai_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22OpenAI%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22anthropic_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Anthropic%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22gemini_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Google%20Gemini%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22groq_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Groq%20API%20Key%22%2C%22password%22%3Atrue%7D%2C%7B%22id%22%3A%22deepseek_key%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22DeepSeek%20API%20Key%22%2C%22password%22%3Atrue%7D%5D%7D)

### Configure for Claude.app

```json
{
  "mcpServers": {
    "agile-team": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/danielscholl/agile-team-mcp-server@main",
        "just-prompt",
        "--default-models",
        "high,openai:o4-mini:high,anthropic:claude-3-7-sonnet-20250219:4k,gemini:gemini-2.5-pro-preview-03-25,gemini:gemini-2.5-flash-preview-04-17"
      ],
      "env": {
        "OPENAI_API_KEY": "<YOUR_OPENAI_KEY>",
        "ANTHROPIC_API_KEY": "<YOUR_ANTHROPIC_KEY>",
        "GEMINI_API_KEY": "<YOUR_GEMINI_KEY>",
        "GROQ_API_KEY": "<YOUR_GROQ_KEY>",
        "DEEPSEEK_API_KEY": "<YOUR_DEEPSEEK_KEY>",
        "OLLAMA_HOST": "http://localhost:11434"
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
    "args": ["--from", "git+https://github.com/danielscholl/agile-team-mcp-server@main", "just-prompt", "--default-models", "high,openai:o4-mini:high,anthropic:claude-3-7-sonnet-20250219:4k,gemini:gemini-2.5-pro-preview-03-25,gemini:gemini-2.5-flash-preview-04-17"]
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

## Available Tools

### List Available Options

Check which providers and models are available for use.

```bash
# List all providers
list_providers_tool

# List models for a specific provider
list_models_tool: "openai"
```

### Send Prompts to Models

Process prompts from input message.

> Default decision maker model: `openai:o4-mini`

**Usage examples:**
```bash
# Basic prompt with default model
prompt_tool: "ping"

# Claude with 4k thinking tokens
prompt_tool: "Analyze quantum computing applications" ["a:claude-3-7-sonnet-20250219:4k"]

# OpenAI with high reasoning effort
prompt_tool: "Write a function to calculate the factorial of a number" ["openai:o3-mini:high"]

# Gemini with 8k thinking budget
prompt_tool: "Evaluate climate change solutions" ["gemini:gemini-2.5-flash-preview-04-17:8k"]
```

- Default decision maker model: `openai:o4-mini`

### Work with Files

Process prompts from files and save responses to files for batch processing.

> Default decision maker model: `openai:o4-mini`

```bash
# Send prompt from file
prompt_from_file_tool: [a:claude-3-7-sonnet] "prompts/function.md"

# Save responses to files
prompt_from_file_to_file_tool: "prompts/uv_script.md"
prompt_from_file_to_file_tool: [a:claude-3-7-sonnet] "prompts/uv_script.md" "prompts/responses/uv_script.py"
prompt_from_file_to_file_tool: [a:claude-3-7-sonnet] "prompts/diagram_request.txt" output_extension="md"
```

### Team Decision Making

Use multiple models as team members to generate different solutions, then have a decision maker model evaluate and choose the best approach.

> Default team member models: `["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro"]`
> Default decision maker model: `openai:o4-mini`

```bash
decision_maker_tool: "prompts/decision.md" ["o:gpt-4.1", "a:claude-3-7-sonnet", "g:gemini-2.5-pro"] "o:o4-mini" "prompts/responses/final_decision.md"
```

