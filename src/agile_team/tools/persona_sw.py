"""Spec Writer persona implementation."""

from typing import List, Optional
from agile_team.shared.config import DEFAULT_MODEL, DEFAULT_TEAM_MODELS, DEFAULT_DECISION_MAKER_MODEL, DEFAULT_SW_PROMPT
from agile_team.shared.utils import load_prompt_file
from agile_team.tools.persona_base import persona_base
from agile_team.tools.persona_dm import DEFAULT_PERSONA_PROMPT

# Load prompts from files
DEFAULT_SW_PROMPT_CONTENT = load_prompt_file("sw_prompt.md")
DEFAULT_SW_DECISION_PROMPT = load_prompt_file("sw_decision_prompt.md")


def persona_sw(
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
    Spec Writer persona implementation.
    
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
    return persona_base(
        persona_name="spec_writer",
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