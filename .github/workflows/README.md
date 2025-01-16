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
and that the following workflows are present in the repository (cf. [below](#installation-of-the-release-pipeline)):
- 'Bump version' (referencing [this workflow](https://github.com/MannLabs/alphashared/blob/main/.github/workflows/bump_version.yml))
- 'Create Draft Release' (referencing [this workflow](https://github.com/MannLabs/alphashared/blob/main/.github/workflows/create_release.yml))
- 'Publish on PyPi' (referencing [this workflow](https://github.com/MannLabs/alphashared/blob/main/.github/workflows/publish_on_pypi.yml))
- 'Publish Docker Image' (referencing [this workflow](https://github.com/MannLabs/alphashared/blob/main/.github/workflows/publish_docker_image.yml))

## Versioning
When a new release is prepared, the version number should be set to `X.Y.(Z+1)`, `X.(Y+1).Z`,
or `(X+1).Y.Z`, depending on the scope of the release: increment `Z` for bug fixes, `Y` for new features, 
`X` for breaking changes. Note: only large-scale breaking changes will increment `X`,
renaming config keys or API parameters will not, so strictly speaking we're not
doing [semantic versioning](https://semver.org/).

After a version `X.Y.Z` is released, the version number in the 
code should be bumped to `X.Y.(Z+1)-dev0`.
For each release the code will be tagged with `v<version number>`.

### Pre-releases
A pre-release does not have public release page on GitHub, but is uploaded to pypi 
(however, it will only be installed if the `--pre` flag is passed to `pip`, i.e. `pip install --pre <packagename>`).
This mechanism is meant to speed up the internal development.
If a pre-release of `X.Y.Z-dev0` is done, the next version number should be `X.Y.Z-dev1`.

(Note: if you want to build wheel from such a version, you need to substitute `-dev` with `.dev`,
to have e.g. `packaname-1.2.3.dev0-py3-none-any.whl`)


### Step-by-step instructions
SR=standard release, PR=pre-release

1. [SR only] Bump the version (e.g. using the 'Bump version') workflow (e.g. to `X.Y.Z`), 
and merge the first resulting PR to `main`.
This version will determine the version of the release and the corresponding tag (e.g. `vX.Y.Z`).
2. Manually run the 'Create Draft Release' workflow in your repository
(in GitHub UI: "Actions" -> Workflow "Create Draft Release" -> "Run Workflow")
to create a new draft release on GitHub: this will create the draft release page and build the installers. 
When running the workflow you can specify an optional input parameter, which is
the full commit hash or branch to release (defaults to `main`).
3. After the workflow ran successfully, it uploads the installer packages as artifacts to the draft
release page. You can download and test these installers manually (in addition to the tests done by the workflow).
4. [SR only] on the GitHub page of the draft release, add release notes (all changes from the last standard release 
to the current release) and then publish the release. This will tag the code.
4. [PR only] Click "Set as a pre-release", leave the release notes blank and then publish the release. This will tag the code.
5. Run the 'Publish on PyPi' workflow, specifying the release tag (e.g. `vX.Y.Z`) as an input parameter.
6. [SR only] Merge the second PR created by the 'Bump version' workflow, which prepares
the next development version (i.e. `X.Y.(Z+1)-dev0`).
6. [PR only] Bump the version to `X.Y.Z)-dev(N+1)`

Note the subtle difference: for a prerelease, you bump the version AFTER the release, for a standard release,
you bump the version BEFORE the release and AFTER.

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
- a valid `.bumpversion.toml` file in the root of the repository, including
[support for pre-release versions](https://github.com/callowayproject/bump-my-version?tab=readme-ov-file#add-support-for-pre-release-versions),
with
```yaml
[tool.bumpversion.parts.pre_l]
# 'final' is just a dummy, but required to have the versioning compatible with the reusable alphashared workflow
values = ["dev", "final"]
optional_value = "final"  
```
(see [alphadia/.bumpversion.toml](https://github.com/MannLabs/alphadia/blob/main/.bumpversion.toml) for an example)

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

Note that it is not necessary to clone the `alphashared` repository. 

#### 'Bump version' workflow
1. Create a new github action `bump_version.yml` in `.github/workflows` that references 
the reusable workflow defined here:
```yaml
# Bump the version for releases
name: Bump version

on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: 'Bump type'
        required: true
        default: 'minor'
        type: choice
        options:
        - prerelease
        - patch
        - minor
        - major

jobs:
  bump-version:
    uses: MannLabs/alphashared/.github/workflows/bump_version.yml@v1
    secrets: inherit
    with:
     bump_type: ${{ inputs.bump_type }}
```

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
      test_stable: true
      only_testpypi_release: false
      skip_macos_arm64_build: false
      # src_folder: src      
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
