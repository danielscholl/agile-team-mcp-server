"""Centralized configuration for the Agile Team MCP Server."""

# Default single model for all tools
DEFAULT_MODEL = "openai:gpt-4o-mini"

# Default team models for multi-model scenarios
DEFAULT_TEAM_MODELS = ["openai:gpt-4.1", "anthropic:claude-3-7-sonnet", "gemini:gemini-2.5-pro-preview-03-25"]

# Default decision maker model
DEFAULT_DECISION_MAKER_MODEL = "openai:gpt-4o-mini"

# Default Product Manager prompt
DEFAULT_PM_PROMPT = "pm_prompt.md"