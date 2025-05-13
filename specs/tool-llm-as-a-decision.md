Feature Request: LLM as a Decision

## Implementation Notes

- Create a new tool 'decision_maker' in src/agile_team/tools/decision_maker.py
- Definition decision_maker(from_file: str, output_dir: str = ., models_prefixed_by_provider: List[str] = None, decision_maker_model: str = DEFAULT_DECISION_MAKER_MODEL, decision_prompt: str = DEFAULT_DECISION_PROMPT) -> None:
- Use the existing prompt_from_file_to_file function to generate responses from 'team members' aka models_prefixed_by_provider.
- Then run the decision_prompt (xml style prompt) with the team members' responses, and the original question prompt to get a decision.
- DEFAULT_DECISION_PROMPT is
  ```xml
        <purpose>
            You are the decision maker of the agile team. You are given a list of responses from your team members. Your job is to take in the original question prompt, and each of the team members' responses, and choose the best direction for the team.
        </purpose>
        <instructions>
            <instruction>Each team member has proposed an answer to the question posed in the prompt.</instruction>
            <instruction>Given the original question prompt, and each of the team members' responses, choose the best answer.</instruction>
            <instruction>Tally the votes of the team members, choose the best direction, and explain why you chose it.</instruction>
            <instruction>To preserve anonymity, we will use model names instead of real names of your team members. When responding, use the model names in your response.</instruction>
            <instruction>As a decision maker, you breakdown the decision into several categories including: risk, reward, timeline, and resources. In addition to these guiding categories, you also consider the team members' expertise and experience. As a bleeding edge decision maker, you also invent new dimensions of decision making to help you make the best decision for your company.</instruction>
            <instruction>Your final decision maker response should be in markdown format with a comprehensive explanation of your decision. Start the top of the file with a title that says "Team Decision", include a table of contents, briefly describe the question/problem at hand then dive into several sections. One of your first sections should be a quick summary of your decision, then breakdown each of the team members' decisions into sections with your commentary on each. Where we lead into your decision with the categories of your decision making process, and then we lead into your final decision.</instruction>
        </instructions>
        
        <original-question>{original_prompt}</original-question>
        
        <team-decisions>
            <team-response>
                <model-name>...</model-name>
                <response>...</response>
            </team-response>
            <team-response>
                <model-name>...</model-name>
                <response>...</response>
            </team-response>
            ...
        </team-decisions>
    ```
- DEFAULT_DECISION_MAKER_MODEL is openai:o4-mini
- The prompt_from_file_to_file will output a file for each team member's response in the output_dir.
- Once they've been created, the decision_prompt will read in the team members' responses, and the original question prompt into the decision_prompt and make another call with the decision_maker_model to get a decision. Write the decision to a file in the output_dir/decision_maker_decision.md.
- Be sure to validate this functionality with uv run pytest <path-to-test-file>
- After you implement update the README.md with the new tool's functionality and run `git ls-files` to update the directory tree in the readme with the new files.
- Make sure this functionality works end to end. This functionality will be exposed as an MCP tool in the server.py file.

## Relevant Files
- src/agile_team/server.py
- src/agile_team/tools/decision_prompt.py
- src/agile_team/tools/prompt_from_file_to_file.py
- src/agile_team/tools/prompt_from_file.py
- src/agile_team/tools/prompt.py
- src/agile_team/shared/llm_providers/openai.py
- src/agile_team/shared/shared/utils.py
- src/agile_team/tests/tools/test_decision_prompt.py

## Validation (Close the Loop)
> Be sure to test this new capability with uv run pytest.

- `uv run pytest src/agile_team/tests/tools/test_decision_prompt.py`
- `uv run just-prompt --help` to validate the tool works as expected.