# Requirements handling in AlphaX

The basic idea is to have two flavours of installation of AlphaX packages: one "loose" version with minimal constraints on the
dependencies, and one "stable" versions, with all dependencies pinned. 
The former is useful for integration an AlphaX package into an existing python environment, while the latter 
should be used whenever reproducibility is key (e.g. to build installers or for production versions).
The dependencies are defined in files
`requirements[_extra].txt` and `_requirements[_extra].freeze.txt`, respectively, which are expected to be in the
`requirements` folder of a package.

## Updating requirements
An update of dependencies can have two main reasons: actively changing dependencies in `requirements[_extra].txt` 
(e.g. adding/removing a dependency or changing a version constraint) or updating the "frozen" dependencies to the latest 
versions (e.g. due to security updates).

In both cases, running the `update_requirements` action will update the "frozen" dependencies and create a PR with the changes.
Note that currently, it needs to be run for different file names (e.g. `requirements.txt` and `requirements_extra.txt`) separately.

## Dockerized version
For local runs, there's a dockerize version: see `Dockerfile` and instructions therein.  