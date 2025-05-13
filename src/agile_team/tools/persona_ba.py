"""Business Analyst persona implementation."""

from typing import List
from agile_team.shared.config import DEFAULT_MODEL, DEFAULT_TEAM_MODELS, DEFAULT_DECISION_MAKER_MODEL
from agile_team.tools.persona_base import persona_base
from agile_team.tools.persona_dm import DEFAULT_PERSONA_PROMPT

# Default Business Analyst prompt template
DEFAULT_BA_PROMPT = """
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
"""


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