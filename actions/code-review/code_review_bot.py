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

MODEL_NAME = "claude-3-5-sonnet-20241022"
MAX_NUM_OUTPUT_TOKENS = 4096


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

    def get_review_feedback(self, changed_files_str, patches_str: str) -> str:
        """
        Sends the content to Claude and gets the review feedback.
        """
        try:
            message = self.anthropic_client.messages.create(
                model=MODEL_NAME,
                max_tokens=MAX_NUM_OUTPUT_TOKENS,
                system=self.system_message,
                messages=[
                    {"role": "user", "content": f"{self.review_prompt}"},
                    {"role": "user", "content": f"{changed_files_str}"},
                    {"role": "user", "content": f"{patches_str}"},
                ],
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
            # Get answer from Claude
            answer = self.get_review_feedback(changed_files_str, patches_str)

            answer_pretty = self._replace(str(answer))
            print(f"Answer: {answer_pretty}")

            text = answer.content[0].text

            with open(f"{self.github_workspace_path}/answer.txt", "w") as f:
                f.write(answer_pretty)
                print(f"wrote answer to file {self.github_workspace_path}/answer.txt")

            repo = self.github_client.get_repo(repo_name)
            pull_request = repo.get_pull(pr_number)

            self.post_review_comments(pull_request, text)

            input_tokens = answer.usage.input_tokens
            output_tokens = answer.usage.output_tokens
            general_text = f"Number of tokens: {input_tokens=} {output_tokens=} {MAX_NUM_OUTPUT_TOKENS=}"
            if (stop_reason := answer.stop_reason) != "end_turn":
                general_text += f"\nPremature stop because: {stop_reason}."
            pull_request.create_issue_comment(general_text)

        except Exception as e:
            self.logger.error(f"Error processing pull request: {str(e)}")
            raise


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
