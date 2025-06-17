"""Tests for MCP server prompts."""

import pytest
from agile_team.server import list_mcp_assets


def test_list_mcp_assets():
    """Test the list_mcp_assets prompt returns comprehensive server information."""
    content = list_mcp_assets()
    
    # Check basic structure
    assert isinstance(content, str)
    assert len(content) > 0
    
    # Check that it includes the main sections
    assert "# 🚀 Agile Team MCP Server Assets" in content
    assert "## 📝 Prompts" in content
    assert "## 🔧 Tools" in content
    assert "## 🏢 Supported LLM Providers" in content
    assert "## 🎯 Quick Start Agile Team Workflow" in content
    
    # Check that all current tools are documented
    assert "prompt_tool" in content
    assert "prompt_from_file_tool" in content
    assert "prompt_from_file2file_tool" in content
    assert "list_providers_tool" in content
    assert "list_models_tool" in content
    assert "persona_ba_tool" in content
    assert "persona_pm_tool" in content
    assert "persona_sw_tool" in content
    assert "persona_dm_tool" in content
    
    # Check that all supported providers are documented
    assert "OpenAI" in content
    assert "Anthropic" in content
    assert "Google Gemini" in content
    assert "Groq" in content
    assert "DeepSeek" in content
    assert "Ollama" in content
    
    # Check provider shortcuts are documented
    assert "`o`" in content  # OpenAI shortcut
    assert "`a`" in content  # Anthropic shortcut
    assert "`g`" in content  # Gemini shortcut
    assert "`q`" in content  # Groq shortcut
    assert "`d`" in content  # DeepSeek shortcut
    assert "`l`" in content  # Ollama shortcut
    
    # Check workflow sections are present
    assert "Business Analysis" in content
    assert "Product Management" in content
    assert "Specification" in content
    assert "Team Decision Making" in content
    
    # Check persona capabilities are documented
    assert "Business Analyst" in content
    assert "Product Manager" in content
    assert "Spec Writer" in content
    assert "Decision Maker" in content
    
    # Check practical examples are included
    assert "persona_ba_tool" in content
    assert "from_file=" in content
    assert "models_prefixed_by_provider=" in content
    
    # Check pro tips and best practices are included
    assert "Pro Tips" in content
    assert "Best Practices" in content
    assert "Model Selection Strategy" in content
    
    # Check it ends with a call to action
    assert "Ready to build your next project" in content


def test_list_mcp_assets_comprehensive_tool_coverage():
    """Test that list_mcp_assets documents all available tools with proper descriptions."""
    content = list_mcp_assets()
    
    # Define expected tools and check they're all documented
    expected_tools = [
        ("prompt_tool", "Send text prompts to multiple LLM models"),
        ("prompt_from_file_tool", "Send prompts from files to models"),
        ("prompt_from_file2file_tool", "Process prompts from files and save responses"),
        ("list_providers_tool", "List all supported LLM providers"),
        ("list_models_tool", "List available models for a specific provider"),
        ("persona_ba_tool", "Business Analyst persona"),
        ("persona_pm_tool", "Product Manager persona"),
        ("persona_sw_tool", "Spec Writer persona"),
        ("persona_dm_tool", "Team Decision Maker")
    ]
    
    for tool_name, expected_description_part in expected_tools:
        assert tool_name in content, f"Tool {tool_name} not found in documentation"
        # Check that some part of the expected description is present
        assert any(word in content for word in expected_description_part.split()), \
            f"Description for {tool_name} not found or incomplete"


def test_list_mcp_assets_provider_documentation():
    """Test that all LLM providers are properly documented with examples."""
    content = list_mcp_assets()
    
    # Expected provider information
    expected_providers = [
        ("OpenAI", "o", "openai", "o:gpt-4o-mini"),
        ("Anthropic", "a", "anthropic", "a:claude-3-5-haiku"),
        ("Google Gemini", "g", "gemini", "g:gemini-2.5-pro-exp"),
        ("Groq", "q", "groq", "q:llama-3.1-70b-versatile"),
        ("DeepSeek", "d", "deepseek", "d:deepseek-coder"),
        ("Ollama", "l", "ollama", "l:llama3.1")
    ]
    
    for provider_name, short_prefix, full_prefix, example_usage in expected_providers:
        assert provider_name in content, f"Provider {provider_name} not documented"
        assert f"`{short_prefix}`" in content, f"Short prefix {short_prefix} not documented"
        assert f"`{full_prefix}`" in content, f"Full prefix {full_prefix} not documented"
        assert example_usage in content, f"Example usage {example_usage} not documented"


def test_list_mcp_assets_workflow_documentation():
    """Test that the agile team workflow is properly documented."""
    content = list_mcp_assets()
    
    # Check that the workflow steps are in logical order
    ba_index = content.find("persona_ba_tool")
    pm_index = content.find("persona_pm_tool") 
    sw_index = content.find("persona_sw_tool")
    dm_index = content.find("persona_dm_tool")
    
    # Business Analyst should come first in the workflow
    assert ba_index < pm_index, "BA tool should be documented before PM tool in workflow"
    # Decision Maker workflow should be separate and documented
    assert dm_index > 0, "Decision Maker workflow should be documented"
    
    # Check workflow includes file references
    assert "requirements/" in content or "concept.md" in content
    assert "responses/" in content
    assert "from_file=" in content
    
    # Check advanced workflows are documented
    assert "Multi-Model Analysis" in content
    assert "Team-Based Persona Decision Making" in content
    assert "File-to-File Processing" in content


def test_list_mcp_assets_structure_and_formatting():
    """Test that the content is well-structured with proper markdown formatting."""
    content = list_mcp_assets()
    
    # Check for proper markdown headers
    assert content.startswith("# 🚀")  # Main title
    assert "## 📝 Prompts" in content  # Section headers
    assert "## 🔧 Tools" in content
    assert "### Core Prompt Tools" in content  # Subsection headers
    
    # Check for code blocks
    assert "```" in content  # Should have code examples
    
    # Check for proper bullet points
    assert "• **" in content  # Bullet points with emphasis
    
    # Check for table formatting
    assert "| Provider |" in content  # Table headers
    assert "|----------|" in content  # Table separators
    
    # Check that sections are properly separated
    assert "---" in content  # Section dividers
    
    # Check for emojis in section headers (part of the design)
    emoji_sections = ["🚀", "📝", "🔧", "🏢", "🎯", "🔄", "💡", "📊"]
    for emoji in emoji_sections:
        assert emoji in content, f"Section with emoji {emoji} not found"