import os
import json
import logging
import re
import sys
import traceback
import anthropic
import untruncate_json
from github import Github
from github.PullRequest import PullRequest

OUTPUT_TOKENS = 'output_tokens'
MODEL = 'model'
THINKING_TOKENS = 'thinking_tokens'


DEFAULT_MODEL_NAME = "claude-3-7-sonnet-latest"
MAX_NUM_OUTPUT_TOKENS = 20000
DEFAULT_NUM_OUTPUT_TOKENS = 4096
MIN_NUM_THINKING_TOKENS = 1024  # https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#important-considerations-when-using-extended-thinking

class CodeReviewBot:
    def __init__(self):
        # Initialize with environment variables
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.review_prompt = os.environ.get("CODE_REVIEW_PROMPT")
        self.system_message = os.environ.get("CODE_REVIEW_SYSTEM_MESSAGE")
        self.github_workspace_path = os.environ.get("GITHUB_WORKSPACE_PATH")

        if not all(
            [
                self.anthropic_api_key,
                self.github_token,
                self.review_prompt,
                self.github_workspace_path,
                self.system_message,
            ]
        ):
            raise ValueError("Missing required environment variables")

        # Initialize clients
        self.anthropic_client = anthropic.Client(api_key=self.anthropic_api_key)
        self.github_client = Github(self.github_token)

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def extract_review_instructions(self, pr_description):
        """Extract review instructions from PR description if present."""
        print(f"pr_description '{pr_description}'")
        if not pr_description:
            return None,  None

        # Look for fenced code block with code-review
        block_match = re.search(r"```code-review\s*\n(.*?)\n```", pr_description, re.DOTALL)
        if block_match:
            instructions = block_match.group(1).strip()
            return self.extract_dict_from_instructions(instructions)
        return None, None

    def extract_dict_from_instructions(self, input_string: str, keys=[MODEL, THINKING_TOKENS, OUTPUT_TOKENS]):
        """Extract a dictionary with special keys from the instructions."""
        extracted_dict = {}
        remaining_lines = []
        for line in input_string.split('\n'):
            found = False
            for key in keys:
                if f"{key}:" in line:
                    extracted_dict[key] = line.split(":", maxsplit=1)[1].strip()
                    found = True
            if not found:
                remaining_lines.append(line)
        return "\n".join(remaining_lines), extracted_dict
    
    def get_review_feedback(self, changed_files_str, patches_str, config, pr_instructions=None):
        """
        Sends the content to Claude and gets the review feedback.
        Now includes PR instructions if provided.
        """
        try:
            messages = [
                {"role": "user", "content": f"{self.review_prompt}"},
                {"role": "user", "content": f"{changed_files_str}"},
                {"role": "user", "content": f"{patches_str}"},
            ]

            # Add PR instructions if available
            if pr_instructions:
                instructions_message = {
                    "role": "user",
                    "content": f"Additional review instructions from the PR description:\n\n{pr_instructions}",
                }
                messages.append(instructions_message)

            if (thinking_tokens := int(config.get(THINKING_TOKENS))) is not None:
                thinking_params = {"thinking" : {
                    "type": "enabled",
                    "budget_tokens": max(thinking_tokens, MIN_NUM_THINKING_TOKENS)
                }}
                print("thinking_params", thinking_params)
            else:
                thinking_params = {}

            max_tokens = int(config.get(OUTPUT_TOKENS, DEFAULT_NUM_OUTPUT_TOKENS))

            message = self.anthropic_client.messages.create(
                model=config.get(MODEL, DEFAULT_MODEL_NAME),
                max_tokens=max_tokens,
                system=self.system_message,
                messages=messages,
                **thinking_params
            )
            return message

        except Exception as e:
            self.logger.error(f"Error getting review feedback: {str(e)}")
            return f"Error during code review: {str(e)}"

    def _extract_json(self, text: str) -> str:
        """Extract the JSON string from the answer."""
        start_rect = text.find("[")
        end_rect = text.rfind("]")
        start_curly = text.find("{")
        end_curly = text.rfind("}")

        if (start_rect != -1 and start_curly > start_rect) and (
            end_rect != -1 and end_rect > end_curly
        ):
            # [{}]
            return text[start_rect : end_rect + 1]
        if (start_curly != -1) and (end_curly != -1):
            # forgot rectangular brackets?
            return "[" + text[start_curly : end_curly + 1] + "]"
        return ""  # Return empty string if no brackets found

    def _get_valid_json(self, json_string: str) -> list[dict[str, str]]:
        """Get valid JSON from the string."""
        try:
            json_string = self._extract_json(json_string)

            json_items = json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Error (1) decoding JSON: {e}")

            self._print_json_context(e, json_string)

            json_string = (
                json_string.replace("`", "")  # Replace backticks
            )
            # json could be truncated due to token limit
            json_string = untruncate_json.complete(json_string)

            try:
                json_items = json.loads(json_string)

            except json.JSONDecodeError as e:
                print(f"Error (2) decoding JSON: {e}")
                self._print_json_context(e, json_string)

                raise e from e
        return json_items

    def process_answer(self, json_string, pr, last_commit):
        """Process the answer from Claude and post as review comments."""
        try:
            json_items = self._get_valid_json(json_string)
        except Exception as e:
            print(f"Error (3) decoding JSON: {e}")
            return json_string

        unprocessed_items = []
        for json_item in json_items:
            change_id = self._safe_get(json_item, "change_id", "-2")
            print("Processing change_id: ", change_id)

            try:
                comment = self._safe_get(json_item, "comment", "")

                if str(json_item["change_id"]) in ["-1", "-2"]:
                    pr.create_issue_comment(comment)
                else:
                    proposed_code = self._safe_get(json_item, "proposed_code")
                    comment = f"{comment}\n\n```python\n{proposed_code}\n```"

                    file_name = json_item["file_name"]
                    if file_name.startswith("./"):
                        file_name = file_name[2:]

                    line = int(json_item["start_line"])

                    # Claude is not good at providing the exact line
                    done = False
                    count = 0
                    line_offsets = [0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -6, 6, -7, 7, -8, 8, -9, 9, -10, 10] # ruff: noqa
                    while not done:
                        try:
                            pr.create_review_comment(
                                body=comment,
                                commit=last_commit,
                                path=file_name,
                                line=line + line_offsets[count],
                                side="RIGHT",
                            )
                            done = True
                        except Exception:
                            count += 1
                            if count >= len(line_offsets):
                                done = True
                            print(
                                f"Could not create review comment for line offset {line_offsets[count]}"
                            )

                print(f"Successfully processed change_id: {json_item['change_id']}")
            except Exception as e:
                print(f"Error processing json_item: {json_item} - {str(e)}")
                traceback.print_exc()
                unprocessed_items.append(json_item)

        return unprocessed_items

    def _safe_get(self, json_item: dict, key: str, default=None) -> str:
        """Safely get a key from a JSON item."""
        default = default or f"(no {key})"
        return self._replace(str(json_item.get(key, default)))

    def _replace(self, text: str) -> str:
        """Replace placeholders in the text."""
        return (
            text.replace("__LB__", "\n").replace("__DQ__", '"').replace("__SQ__", "'")
        )

    def _print_json_context(self, exception, json_string):
        """Print the JSON context around the error."""
        try:
            number = int(re.search(r"char (\d+)", str(exception)).group(1))
            print(json_string[number - 20 : number + 20])
        except Exception:
            print(f"Error printing JSON context.")

    def post_review_comments(self, pull_request: PullRequest, answer: str):
        """
        Posts the review feedback as comments on the pull request.
        """
        try:
            last_commit = list(pull_request.get_commits())[-1]

            unprocessed_items = self.process_answer(answer, pull_request, last_commit)

            unprocessed_text = (
                unprocessed_items
                if isinstance(unprocessed_items, str)
                else "\n\n```\n".join([json.dumps(i) for i in unprocessed_items])
            )

            if unprocessed_text:
                text = (
                    "The following feedback could not be added to specific lines, but still contains valuable information:\n\n"
                    + "```\n"
                    + self._replace(unprocessed_text)
                    + "\n```"
                )
                pull_request.create_issue_comment(text)

            self.logger.info("Successfully posted review comments")
        except Exception as e:
            self.logger.error(f"Error posting review comments: {str(e)}")

    # async \
    def process_pull_request(
        self, changed_files_str: str, patches_str: str, repo_name: str, pr_number: int
    ):
        """
        Main method to process a pull request.
        """
        try:
            repo = self.github_client.get_repo(repo_name)
            pull_request = repo.get_pull(pr_number)

            # Extract PR description and get review instructions if any
            pr_description = pull_request.body
            review_instructions, config = self.extract_review_instructions(pr_description)

            if review_instructions:
                print(
                    f"Found review instructions in PR description: {review_instructions} {config=}"
                )

            # Get answer from Claude
            raw_answer = self.get_review_feedback(
                changed_files_str, patches_str, config, review_instructions
            )
            print(f"{raw_answer=}")
            answer, thinking = self.parse_answer(raw_answer)
            print(f"{answer=}")
            print(f"{thinking=}")
            answer_pretty = self._replace(str(answer))
            print(f"{answer_pretty=}")

            text = answer.content[0].text

            with open(f"{self.github_workspace_path}/answer.txt", "w") as f:
                f.write(answer_pretty)
                print(f"wrote answer to file {self.github_workspace_path}/answer.txt")

            self.post_review_comments(pull_request, text)

            input_tokens = answer.usage.input_tokens
            output_tokens = answer.usage.output_tokens
            max_tokens = config.get(OUTPUT_TOKENS, DEFAULT_NUM_OUTPUT_TOKENS)
            general_text = (
                f"Number of tokens: {input_tokens=} {output_tokens=} {max_tokens=}"
                f"\n{review_instructions=}"
                f"\n{config=}"
                f"\nthinking: ```\n{thinking}\n```"
            )
            if (stop_reason := answer.stop_reason) != "end_turn":
                general_text += f"\nPremature stop because: {stop_reason}."
            pull_request.create_issue_comment(general_text)

        except Exception as e:
            self.logger.error(f"Error processing pull request: {str(e)}")
            raise

    def parse_answer(self, raw_answer):
        """Parse the answer from Anthropic API, which may include thinking tokens."""
        answer = []
        thinking = []
        for item in raw_answer.content:
            if item.type == "thinking" or item.type == "redacted_thinking":
                thinking.append(item)
            else:
                answer.append(item)

        return answer, thinking



def read_file(file_path: str) -> str:
    """Read a file and returns its content as a string."""

    file_path = file_path.strip()

    if not os.path.exists(file_path):
        raise ValueError(f"File '{file_path}' does not exist.")

    if os.path.isfile(file_path):
        with open(file_path, "r") as infile:
            return infile.read()

    raise ValueError(f"Error reading file '{file_path}'")


def main():
    """
    Main function to be called by GitHub Action.
    """
    github_repository = os.environ.get("GITHUB_REPOSITORY")
    pull_request_number = int(os.environ.get("GITHUB_EVENT_NUMBER"))

    changed_files_str = read_file(sys.argv[1])
    patches_str = read_file(sys.argv[2])

    bot = CodeReviewBot()
    bot.process_pull_request(
        changed_files_str, patches_str, github_repository, pull_request_number
    )


if __name__ == "__main__":
    main()
