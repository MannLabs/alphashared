# AlphaX Release Process

## Release a new version
### Tagging of changes
In order to have release notes automatically generated, changes need to be tagged with labels.
The following labels are used (should be safe-explanatory):
`breaking-change`, `bug`, `enhancement`.

### Release a new version
Note: Releases need to be done from the `main` branch.

1. Bump the version locally to (e.g. to `X.Y.Z`) and merge the change to `main`.
2. Create a new draft release on GitHub using the
[Create Draft Release](https://github.com/MannLabs/alphashared/.github/workflows/create_release.yml) workflow.
You need to specify the commit to release, and the release tag (e.g. `vX.Y.Z`).
3. Test the release manually.
4. Add release notes and publish the release on GitHub.
5. Run the [Publish on PyPi](https://github.com/MannLabs/alphashared/.github/workflows/publish_on_pypi.yml) workflow,
specifying the release tag (e.g. `vX.Y.Z`).
6. (optional, if present) Run the [Publish Docker Image](https://github.com/MannLabs/alphashared/.github/workflows/publish_docker_image.yml) workflow,
specifying the release tag (e.g. `vX.Y.Z`).


## Installation of the release pipeline
### Requirements on the caller repository
In order to be compatible with the workflow, the calling repository must meet the following requirements:

#### Version
The file `<package_name>/__init__.py` must contain the following line:

```python
__version__ = "<version to release, e.g. 1.2.3>"
```

#### Install scripts
The workflow looks for platform-specific subdirectories `linux`, `macos`, `windows` in the
`release` directory of the calling repository. If the directory exists, an artifact is build for that platform.
The subdirectories must contain the following scripts:

```
release/<platform>/build_installer_<platform>.sh
release/<platform>/build_package_<platform>.sh
release/<platform>/build_gui_<platform>.sh (optional)
```
or `.ps1` if platform is `windows`.



### Installation
1. Create a new github action in `.github/workflows` like this:
```yaml
# Create a draft release and build and upload all installers to it.

on:
  workflow_dispatch:
    inputs:
      commit_to_release:
        description: 'Enter commit hash to release (example: ef4037cb571f99cb4919b520fde7174972aae473)'
        type: string
        required: true
      tag_to_release:
        description: 'Enter tag of the new release to create (example: v1.5.5). The code version needs to be bumped already tom atch the tag.'
        type: string
        required: true

jobs:
  create-release:
    uses: MannLabs/alphashared/.github/workflows/create_release.yml@v1
    with:
      # see the documentation of the action for more information on the parameters
      package_name: peptdeep
      commit_to_release: ${{ inputs.commit_to_release }}
      tag_to_release: ${{ inputs.tag_to_release }}
      # optional parameters
      build_nodejs_ui: false
      test_app: false
      python_version: 3.11
    secrets: inherit
```


## Development
If you need to change the basic workflow, after merging to `main`, create a new `TAG`
```bash
TAG=v2
git tag $TAG -f ; git push origin --tags
```
and update it in the calling repositories (-> `uses: .../create_release.yml@v1` -> `uses: .../create_release.yml@v1`)

If the change is non-breaking, you can overwrite an existing tag:
```bash
TAG=v1
git push --delete origin $TAG; git tag $TAG -f ; git push origin --tags
```