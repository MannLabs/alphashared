"""Format data of a given pull request to a AI-readable format.

Required environment:
- GITHUB_EVENT_NUMBER: The number of the pull request.
- GITHUB_REPOSITORY: The repository of the pull request.
- GITHUB_TOKEN: The token to authenticate with the GitHub API.

Required arguments:
- whitespace-separated list of relative paths of files changed in the pull request.

Returns
-------
- A formatted string containing the data of the pull request.
"""

import os
import sys

from github import Github, File

g = Github(os.environ["GITHUB_TOKEN"])
repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])
pr = repo.get_pull(int(os.environ["GITHUB_EVENT_NUMBER"]))


def _get_file_content(file_path: str, commit_sha: str) -> str:
    """Get the content of a file in a specific commit."""
    try:
        return repo.get_contents(file_path, ref=commit_sha).decoded_content.decode()
    except Exception:  # if file doesn't exist in that commit
        return ""


def _get_file_patch(file: File) -> str:
    """Get the patch of a file."""
    return file.patch if file.patch else "Binary file or no patch available"


def _format_pr(pr_data: list[dict[str, str]]) -> str:
    """Format the data of the pull request to a AI-readable format."""
    pr_contents = ["=============", "START ALL PATCHES:", ""]

    for item in pr_data:
        file_name = item["file_name"]
        prefix = "" if file_name.startswith("./") else "./"

        pr_contents.append(
            f"START PATCH FOR FILE: '{prefix}{file_name}' >>>>>>>>>>>>>>>>"
        )
        pr_contents.append(item["patch"])
        pr_contents.append(
            f"<<<<<<<<<<<<<<<< END PATCH FOR FILE: '{prefix}{file_name}'"
        )
        pr_contents.append("")

    pr_contents.append("END ALL PATCHES")
    pr_contents.append("=============")

    return "\n".join(pr_contents)


if __name__ == "__main__":
    changed_files = sys.argv[1].split()
    output_path = sys.argv[2]

    pr_data: list[dict[str, str]] = []
    for file in pr.get_files():
        file_name = file.filename
        if file_name in changed_files:
            original_content = _get_file_content(file_name, pr.base.sha)
            new_content = _get_file_content(file_name, pr.head.sha)
            patch = _get_file_patch(file)
            pr_data.append(
                {
                    "file_name": file_name,
                    "original_content": original_content,
                    "new_content": new_content,
                    "patch": patch,
                }
            )

    formatted_pr = _format_pr(pr_data)

    with open(output_path, "w") as outfile:
        outfile.write(formatted_pr)

# try:
#     review_comments = {file: [(1, 'cool')] for file in changed_files}
#     g = Github(os.environ['GITHUB_TOKEN'])
#     repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
#     pr = repo.get_pull(int(os.environ['GITHUB_EVENT_NUMBER']))
#
#     last_commit = list(pr.get_commits())[-1]
#
#     for file_name, comments in review_comments.items():
#         for line, comment in comments:
#             print("XXX", line, comment)
#             #pr.create_review_comment(body=comment, commit=last_commit, path=file_name, line=int(line))
#
#     print('Code review completed and comments posted.')
# except Exception as e:
#     print(f'Error during code review: {str(e)}')
#     import traceback
#
#     traceback.print_exc()
#     exit(1)

#            response = requests.post(
#                os.environ['REVIEW_API_URL'],
#                json={"files": file_data},
#                headers={
#                    'Authorization': f"Bearer {os.environ['REVIEW_API_KEY']}",
#                    'Content-Type': 'application/json'
#                }
#            )
#            response.raise_for_status()
#            review_comments = response.json()
