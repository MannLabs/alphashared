# get-code-review-input

Creates three artifacts in your github actions that can be passed to a LLM for code review:
- `patches.txt` containing the changes to review
- `all_files.txt` containing the contents of all files
- `changed_files.txt` containing the contents of the changed files only

## Usage
1. Add the following action to your repository (`.github/workflows/code-review.yml`):
```yaml
# checks to run on branches for each pull request
name: code-review

on:
  pull_request:

jobs:
  get-code-review-input:
    runs-on: ubuntu-latest
    steps:
      - uses: MannLabs/alphashared/actions/get-code-review-input@v1
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PR_NUMBER: ${{ github.event.number }}
```
Alternatively, just add the `get-code-review-input` step to an existing workflow.

2. After the action ran on a pull request, you can download the artifacts by clicking 
"Actions" -> (lates workflow run) and navigating to "Artifacts" at the bottom of the page.