import json
import sys
import os

from github import Github
import traceback

def process_json_data(json_string, pr, last_commit):
    try:
        json_items = json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    for json_item in json_items:
        # Validate the structure of each json_item
        required_fields = ['change_id', 'file_name', 'start_line', 'end_line', 'summary', 'reason', 'proposed_code']
        if not all(field in json_item for field in required_fields):
            print(f"Error: Invalid json_item structure for change_id: {json_item.get('change_id', 'unknown')}")
            continue

        # Send each json_item to the API
        try:
            proposed_code = json_item['proposed_code'].replace('__LB__', '\n').replace('__DQ__', '"')
            comment = f"===AUTOMATED===\n{json_item['reason']}\n\n```python\n{proposed_code}\n```"
            file_name = json_item['file_name']
            line = int(json_item["start_line"])
            pr.create_review_comment(body=comment, commit=last_commit, path=file_name, line=line)

            print(f"Successfully processed change_id: {json_item['change_id']}")
        except Exception as e:
            print(f"Error processing change_id: {json_item['change_id']} - {str(e)}")
            traceback.print_exc()
            # dump all that were not applicable to the comments



def main():
    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
    pr = repo.get_pull(int(os.environ['PR_NUMBER']))

    review_data = sys.argv[1]

    try:

        last_commit = list(pr.get_commits())[-1]

        with open(review_data) as f:
            review_data = f.read()
        print("GOT", review_data)
        process_json_data(review_data, pr, last_commit)

        print('Code review completed and comments posted.')
    except Exception as e:
        print(f'Error during code review: {str(e)}')
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()
