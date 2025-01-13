# Automated code reviews
Fully automated code reviews using the [Anthropic AI](https://www.anthropic.com/) API.

## Setup

1. Add the following workflow to your repository and push it to `main`..
In order to function correctly, it needs to be in a separate file, e.g. `.github/workflows/code-review.yml`. 
Note: after adding it to `main`, it works only for branches that have branched off that new version of `main`.
 
```yaml
# checks to run on branches for each pull request
name: code-review

on:
  pull_request:
    types: [ labeled ]

jobs:
  get-code-review:
    runs-on: ubuntu-latest
    if: contains(github.event.pull_request.labels.*.name, 'code-review')
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: MannLabs/alphashared/actions/code-review@v1
        continue-on-error: true
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          CODE_REVIEW_SYSTEM_MESSAGE: ${{ secrets.CODE_REVIEW_SYSTEM_MESSAGE }}
          CODE_REVIEW_PROMPT: ${{ secrets.CODE_REVIEW_PROMPT }}
          GITHUB_EVENT_NUMBER: ${{ github.event.number }}
          EXCLUDED_EXTENSIONS: "ipynb;js"  # optional
```

2. Add a github label `code-review` to a PR that you want to have reviewed.
The action should run and after a while (~2 minutes) add the feedback to your code.

Beware: each code review costs money (order of 0.5 EUR), so use it wisely. Also, it will not perform
well on huge, unfocused PRs (token window and API response token limit).