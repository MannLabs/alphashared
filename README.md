# alphashared
Shared non-production code for AlphaX packages.

## contents
- `actions`: reusable github actions
- `actions/get-code-review-input`: generates input for AI-assisted code review, see [README](actions/get-code-review-input/README.md)

- `.github/workflows`: github workflows
- `.github/workflows/create_release.yml`: reusable workflow for creating releases, see [README](.github/workflows/README.md)
- `.github/workflows/publish_on_pypi.yml`: reusable workflow for publishing on PyPi, see [README](.github/workflows/README.md)
- `.github/workflows/alphatesting.yml`: Cross-project tests for AlphaX, see [README](alphatesting/README.md)