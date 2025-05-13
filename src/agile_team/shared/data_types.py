"""Data types for the Agile Team MCP Server."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class ModelProviders(Enum):
    """
    Enum of supported model providers with their full and short names.
    """
    OPENAI = ("openai", "o")
    ANTHROPIC = ("anthropic", "a")
    GEMINI = ("gemini", "g") 
    GROQ = ("groq", "q")
    DEEPSEEK = ("deepseek", "d")
    OLLAMA = ("ollama", "l")
    TESTING = ("testing", "t")  # Added for testing purposes
    
    def __init__(self, full_name, short_name):
        self.full_name = full_name
        self.short_name = short_name
        
    @classmethod
    def from_name(cls, name):
        """
        Get provider enum from full or short name.
        
        Args:
            name: The provider name (full or short)
            
        Returns:
            ModelProviders: The corresponding provider enum, or None if not found
        """
        for provider in cls:
            if provider.full_name == name or provider.short_name == name:
                return provider
        return None


class ProviderModelRequest(BaseModel):
    """Request model for model/provider operations."""
    models_prefixed_by_provider: List[str] = Field(
        description="List of models in the format provider:model"
    )

    @field_validator("models_prefixed_by_provider")
    @classmethod
    def validate_models_prefixed_by_provider(cls, v: List[str]) -> List[str]:
        """Validate that each entry in models_prefixed_by_provider has the format provider:model."""
        if not v:
            raise ValueError("At least one model must be provided")
        
        for model in v:
            if ":" not in model:
                raise ValueError(
                    f"Invalid model format: {model}. Must be in the format provider:model"
                )
            provider, _ = model.split(":", 1)
            if not provider:
                raise ValueError(
                    f"Invalid model format: {model}. Provider cannot be empty"
                )
        
        return v


class PromptRequest(ProviderModelRequest):
    """Request model for prompt operations."""
    text: str = Field(description="The text prompt to send to the models")


class FilePromptRequest(ProviderModelRequest):
    """Request model for file-based prompt operations."""
    file: str = Field(description="Path to the file containing the prompt")


class FileToFilePromptRequest(FilePromptRequest):
    """Request model for file-to-file prompt operations."""
    output_dir: str = Field(
        default=".",  # This will be overridden in the implementation to use input file's directory
        description="Directory where response files should be saved (defaults to input file's directory if not specified)"
    )
    output_extension: Optional[str] = Field(
        default=None,
        description="File extension for output files (e.g., '.py', '.txt', '.md'). If None, defaults to '.txt'"
    )
    output_path: Optional[str] = Field(
        default=None,
        description="Optional full output path with filename. If provided, the extension from this path will be used."
    )


class ProviderRequest(BaseModel):
    """Request model for provider-specific operations."""
    provider: str = Field(description="The provider to use")