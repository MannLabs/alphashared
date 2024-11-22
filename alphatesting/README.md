# alphatesting
Cross-project tests for AlphaX.
These tests should help to detect breaking changes in the AlphaX projects
before they are released.


## Disclaimer
This approach to catch breaking changes early relies on the assumption that the tests of the individual
projects are comprehensive and cover all relevant aspects of the project. Breaking changes in code parts 
that are not tested will not be detected.

## Basic idea
The following description differentiates "base packages"
(no dependency on other AlphaX packages),
 from "non-base packages" (one or more dependencies on other AlphaX packages).
Examples for base packages are AlphaBase and directLFQ, examples for non-base packages are AlphaDIA and AlphaPeptDeep.

The provided Dockerfile sequentially clones selected AlphaX projects, and checks out a user-defined version
(git commit hash, branch name, latest release). Prior to installing of each non-base project,
the dependencies to all base projects are removed from the requirements file, such that the 
non-base projects use the already provided, user-defined versions of the base projects. 

In this defined python environment, selected tests of base and non-base projects are run.

## Maintenance
Whenever a new project is added to the AlphaX family, that has dependencies to other projects, 
add it to the `Dockerfile` and the workflow file. 

Also, when an already supported AlphaX package gets a new dependency to another AlphaX package,
in the `Dockerfile` adapt the replacements of dependencies in the `requirements` files .

Use the other projects as a template.

When a new class of tests is added, add it to the workflow file. Similarly, when a test run script is renamed,
adapt the workflow file.


## Usage
### How to use this

1. Run [this workflow](https://github.com/MannLabs/alphatesting/actions/workflows/alphatesting.yml)
and optionally specify the git commit hashes or branch names of the supported AlphaX projects.
The default is 'latest', i.e. the latest release.
Note: tags are currently not supported

2. The workflow will build a docker image with the specified versions of the AlphaX projects 
and run the tests.

Currently, the following tests are run:
- `alphabase`
- `alphawraw`
- `alphapeptdeep`
- `alphadia`

If one or more tests failed, the workflow will fail. In this case, inspect the logs of the failed tests.

### Example
You want to release a new version of `alphabase` and want to make sure that the changes do not break the current releases
of the other projects.

In this case, identify the commit hash of the `alphabase` release candidate, and pass it to the
workflow (alternatively, pass `development`, if this branch contains already the changes to be released. 
Leave all other input values at their default.
If all tests run successfully, you got some confidence that the changes in `alphabase` 
do not break the other projects.
