import os
import sys


# import requests
# import subprocess
from github import Github

g = Github(os.environ['GITHUB_TOKEN'])
repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
pr = repo.get_pull(int(os.environ['PR_NUMBER']))

def get_file_content(file_path, commit_sha):
    try:
        return repo.get_contents(file_path, ref=commit_sha).decoded_content.decode()
    except:
        return ""  # Return empty string if file doesn't exist in that commit

def get_file_patch(file):
    return file.patch if file.patch else ""

def format_code_review_data(data_list):
    formatted_string = "Beginning of Code Review Data:\n\n"

    for item in data_list:
        formatted_string += f"=============\n"
        formatted_string += f"Beginning of data for file: {item['filename']}\n"
        formatted_string += "Original Content:\n"
        formatted_string += "```\n"
        formatted_string += item['originalContent']
        formatted_string += "\n```\n\n"
        formatted_string += "Patch:\n"
        formatted_string += "```\n"
        formatted_string += item['patch']
        formatted_string += "\n```\n\n"
        formatted_string += "---\n"
        formatted_string += f"End of data for file: {item['filename']}\n"
        formatted_string += f"=============\n\n"

    formatted_string += "End of Code Review Data"

    return formatted_string

changed_files = sys.argv[1].split()

file_data = []
for file in pr.get_files():
    if file.filename in changed_files:
        original_content = get_file_content(file.filename, pr.base.sha)
        changed_content = get_file_content(file.filename, pr.head.sha)
        patch = get_file_patch(file)
        file_data.append({
            "filename": file.filename,
            "originalContent": original_content,
            "changedContent": changed_content,
            "patch": patch
        })


print("# ##############################################################################")
print(format_code_review_data(file_data))
print("# ##############################################################################")

# try:
#     review_comments = {file: [(1, 'cool')] for file in changed_files}
#     g = Github(os.environ['GITHUB_TOKEN'])
#     repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
#     pr = repo.get_pull(int(os.environ['PR_NUMBER']))
#
#     last_commit = list(pr.get_commits())[-1]
#
#     for filename, comments in review_comments.items():
#         for line, comment in comments:
#             print("XXX", line, comment)
#             #pr.create_review_comment(body=comment, commit=last_commit, path=filename, line=int(line))
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