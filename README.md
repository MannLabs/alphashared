# alphashared
Shared non-production code for AlphaX packages.

## contents
- `actions`: reusable github actions
- `actions/code-review`: AI-assisted code review, see [README](actions/code-review/README.md)
- `actions/get-code-review-input`: (deprecated) generates input for manual AI-assisted code review, see [README](actions/get-code-review-input/README.md)

- `.github/workflows`: github workflows
- `.github/workflows/bump_version.yml`: reusable workflow for bumping versions, see [README](.github/workflows/README.md)
- `.github/workflows/create_release.yml`: reusable workflow for creating releases, see [README](.github/workflows/README.md)
- `.github/workflows/publish_on_pypi.yml`: reusable workflow for publishing on PyPi, see [README](.github/workflows/README.md)
- `.github/workflows/alphatesting.yml`: Cross-project tests for AlphaX, see [README](alphatesting/README.md)