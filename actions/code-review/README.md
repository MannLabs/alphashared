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

To get another review (e.g. because you added more commits, or the first review went sideways, or to try new parameters) 
just remove the label and add it again.

Beware: each code review costs money (order of 0.5 EUR), so use it wisely. Also, it will not perform
well on huge, unfocused PRs (due to context window and API response token limit).

3. (optional) Providing Custom Review Instructions
You can provide specific instructions to the AI reviewer by adding them to your PR description in 
a fenced code block with the tag `code-review`:

```code-review
Answer in a pirate voice.
Focus: performance
Ignore: style
Check for: security vulnerabilities, race conditions
```
These instructions will be passed to the AI along with the code changes to provide more tailored review feedback.

In addition, there's some configurability using special keys:
```code-review
Answer in a pirate voice.
model: <model_name>
thinking_tokens: <number_of_thinking_tokens>
max_tokens: <max_number_of_tokens>
```
with

`model_name`: API model name (default: `claude-3-7-sonnet-latest`). Cf. https://docs.anthropic.com/en/docs/about-claude/models/all-models#model-names 

`thinking_tokens`: number of thinking tokens (default: 0). If given, needs to be >= 1024.

`max_tokens`: maximum number of tokens (output+thinking, default: 4096). Might need to be increased if `thinking_tokens` are used

