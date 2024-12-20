# AlphaX Release Process
These [reusable workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows) aim at unifying the release process for all AlphaX packages.
They automate the creation of a draft release on GitHub, the building of installers for different platforms,
testing of the installers, the publishing of the package on PyPi and (optionally) the publishing on Docker Hub.

The first part of this Readme explains the release process itself.
The second part shows how to incorporate this pipeline into your repository.
The last part explains how to further develop this pipeline.

## Release a new version

### Prerequisites
Note: these instructions assume that the release is done from the `main` branch,
and that the following worklows are present in the repository (cf. [below](#installation-of-the-release-pipeline)):
- 'Create Draft Release' (referencing [this workflow](https://github.com/MannLabs/alphashared/.github/workflows/create_release.yml))
- 'Publish on PyPi' (referencing [this workflow](https://github.com/MannLabs/alphashared/.github/workflows/publish_on_pypi.yml))
- 'Publish Docker Image' (referencing [this workflow](https://github.com/MannLabs/alphashared/.github/workflows/publish_docker_image.yml))


### Step-by-step instructions
1. Bump the version locally to (e.g. to `X.Y.Z`), e.g. using `bumpversion`, and push this change to `main`.
This version will determine the version of the release and the corresponding tag (e.g. `vX.Y.Z`).
2. Manually run the 'Create Draft Release' workflow 
in your repository to create a new draft release on GitHub 
(in GitHub UI: "Actions" -> Workflow "Create Draft Release" -> "Run Workflow").
When running the workflow you can specify an optional input parameter, which is
the full commit hash or branch to release (defaults to `main`).
3. After the workflow ran successfully, it uploads the installer packages as artifacts to the draft
release page. You can download and test these installers manually (in addition to the tests done by the workflow).
4. On the GitHub page of the draft release, add release notes and then publish the release.
5. Similar to before, run the 'Publish on PyPi' workflow, specifying the release tag (e.g. `vX.Y.Z`) as an input parameter.
6. TODO not implemented yet (optional, if present) Run the 'Publish Docker Image' workflow, specifying the release tag 
(e.g. `vX.Y.Z`) as an input parameter.


## Installation of the release pipeline
In order to incorporate this pipeline into your repository, it might help to look at
the following pull requests and the respective workflow files in these repositories:
- https://github.com/MannLabs/alphapeptdeep/pull/206
- https://github.com/MannLabs/alphadia/pull/326
- https://github.com/MannLabs/directlfq/pull/42


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
      commitish_to_release:
        description: 'Enter commit hash or branch to release (default: main).'
        type: string
        required: false

jobs:
  create-release:
    secrets: inherit
    uses: MannLabs/alphashared/.github/workflows/create_release.yml@v1
    with:
      # see the documentation of the action for more information on the parameters
      commitish_to_release: ${{ inputs.commitish_to_release }}
      package_name: <Name of package, e.g. "alphadia", "peptdeep", ..>
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
        description: 'Enter tag to release (example: v1.5.5). A tag with this name must exist in the repository.'
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
      only_testpypi_release: false
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

### Test runs
In order to test the release pipeline, you need to use a 'fresh' release tag, otherwise the pipeline will fail.
As this tag is derived from the code version, an additional step is required to circumvent this:
Set the `DEBUG_RELEASE_WORKFLOW_SUFFIX` **repository variable** to some value (e.g. `test1`) and it will
be appended to the release tag thus making it unique.
Don't forget to remove this variable after your tests finished.

Repository variables can be set in the GiHub Repository "Settings" ->  "Secrets and Variables" ->  "Actions" -> "Variables" Tab -> "Repository variables"
