# AlphaX Release Process
These [reusable workflow](https://docs.github.com/en/actions/sharing-automations/reusing-workflows) aim at unifying the release process for all AlphaX packages.
It automates the creation of a draft release on GitHub, the building of installers for different platforms,
testing of the installers, the publishing of the package on PyPi and (optionally) the publishing on Docker Hub.

The first part of this Readme explains the release process itself.
The second part shows how to incorporate this pipeline into your repository.
The last part explains how to further develop this pipeline.

## Release a new version

### Release a new version
Note: these instructions assume that the release is done from the `main` branch.

1. Bump the version locally to (e.g. to `X.Y.Z`), e.g. using `bumpversion`, and push this change to `main`.
2. Manually run the 'Create Draft Release' workflow 
(the one referencing [this workflow](https://github.com/MannLabs/alphashared/.github/workflows/create_release.yml))
in your repository to create a new draft release on GitHub 
(in GitHub UI: "Actions" -> Workflow "Create Draft Release" -> "Run Workflow").

When running the workflow you will be prompted to specify
- the full commit hash to release (e.g. the latest commit to `main`), and
- the release tag (e.g. `vX.Y.Z`, note the prefixed `v`). The version in this tag must match the code version.
3. After the workflow ran successfully, it uploads the installer packages as artifacts to the draft
release page. You can download and test these installers manually (in addition to the tests done by the workflow).
4. On the GitHub page of the draft release, add release notes and then publish the release.
5. Similar to before, run the 'Publish on PyPi' workflow
(referencing [this](https://github.com/MannLabs/alphashared/.github/workflows/publish_on_pypi.yml)),
specifying the release tag (e.g. `vX.Y.Z`).
6. TODO not implemented yet (optional, if present) Run the 'Publish Docker Image' workflow
(referencing [this](https://github.com/MannLabs/alphashared/.github/workflows/publish_docker_image.yml)),
specifying the release tag (e.g. `vX.Y.Z`).


## Installation of the release pipeline
In order to incorporate this pipeline into your repository, it might help to look at
the following pull request:
- https://github.com/MannLabs/alphapeptdeep/pull/206
- https://github.com/MannLabs/alphadia/pull/326


### Requirements on the caller repository
In order to be compatible with this workflow, the calling repository must meet the following requirements,
which are explained in more detail below:
- the package must have a version number at a defined location
- a `release` directory must exist and contain the necessary scripts for building the packages
- GitHub actions must be created in the `.github/workflows` directory that call the reusable workflows defined in here

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
release/<platform>/build_gui_<platform>.sh (optional)
release/<platform>/build_package_<platform>.sh
```
or `.ps1` if platform is `windows`.

Here, the `build_installer_<platform>.sh` script is responsible for building the installer (using `pyinstaller`), 
the optional `build_gui_<platform>.sh` is to build a GUI (if not already done
by the first script). Last, the `build_package_<platform>.sh` script is responsible for building the package,
i.e. the file that is required to install it on the respective platform (linux: `.deb`, macos: `.pkg`, windows: `.exe`).


### Installation
#### 'Create release' workflow
1. Create a new github action `create_release.yml` in `.github/workflows` that references 
the reusable workflow defined here:
```yaml
# Create a draft release and build and upload all installers to it.
name: Create Draft Release

on:
  workflow_dispatch:
    inputs:
      commit_to_release:
        description: 'Enter commit hash to release (example: ef4037cb571f99cb4919b520fde7174972aae473)'
        type: string
        required: true
      tag_to_release:
        description: 'Enter tag of the new release to create (example: v1.5.5). The code version needs to be bumped already to match the tag.'
        type: string
        required: true

jobs:
  create-release:
    secrets: inherit
    uses: MannLabs/alphashared/.github/workflows/create_release.yml@v1
    with:
      # see the documentation of the action for more information on the parameters
      package_name: <Name of package, e.g. "alphadia", "peptdeep", ..>
      commit_to_release: ${{ inputs.commit_to_release }}
      tag_to_release: ${{ inputs.tag_to_release }}
      # optional parameters
      build_nodejs_ui: true
      test_app: true
      python_version: 3.9
```
Note that it is not necessary to clone the `alphashared` repository. 


#### 'Publish on pypi' workflow
1. Create a new github action `publish_on_pypi.yml` in `.github/workflows` like this:
```yaml
# Publish and test release on Test-PyPI and PyPI.
name: Publish on PyPi

on:
  workflow_dispatch:
    inputs:
      tag_to_release:
        description: 'Enter tag to release (example: v1.5.5). A tag with the same name must exist in the repository.'
        type: string
        required: true

jobs:
  publish_on_pypi:
    uses: MannLabs/alphashared/.github/workflows/publish_on_pypi.yml@v1
    secrets:
      test_pypi_api_token: ${{ secrets.TEST_PYPI_API_TOKEN }}
      pypi_api_token: ${{ secrets.PYPI_API_TOKEN }}
    with:
      # see the documentation of the action for more information on the parameters
      package_name: <Name of package, e.g. "alphadia", "peptdeep", ..>
      tag_to_release: ${{ inputs.tag_to_release }}
      # optional parameters:
      python_version: 3.9
      use_pyproject_toml: false
```


## Developing the reusable release pipeline
If you need to make changes to the reusable workflow 
(e.g. include some extra steps), clone this repository, and commit your changes to
a branch. After merging to `main`, create a new `TAG`
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