# Requirements handling in AlphaX

The basic idea is to have two flavours of installation of AlphaX packages: one "loose" version with minimal constraints on the
dependencies, and one "stable" versions, with all dependencies pinned. 
The former is useful for integration an AlphaX package into an existing python environment, while the latter 
should be used whenever reproducibility is key (e.g. to build installers or for production versions).
Also, this approach allows that the highest-level package (e.g. AlphaDIA) can conveniently freeze its dependencies,
without too much risks of conflicts.

The dependencies are defined in files
`requirements(_some-extra).txt` and `_requirements(_some-extra).freeze.txt`, respectively, which are expected to be in the
`requirements` folder of a package.

## Updating requirements
An update of dependencies can have two main reasons: actively changing dependencies in `requirements[_extra].txt` 
(e.g. adding/removing a dependency or changing a version constraint) or updating the "frozen" dependencies to the latest 
versions (e.g. due to security updates).

In both cases, running the `update_requirements` action will update the "frozen" dependencies and create a PR with the changes.
Note that currently, it needs to be run for different file names (e.g. `requirements.txt` and `requirements_extra.txt`) separately.

## Special cases
Sometimes, dependencies are only available for certain platforms. In the case of e.g. CUDA dependencies, 
they will be added to the "freeze" file as the container used to determine the dependencies is a linux container.

Another special case is the restriction of a dependency version for a certain platform, which requires
multiple lines per dependency.

This can be resolved by adding a file `requirements[_extra].constraints.txt`, e.g.
```
# Constraints file to "requirements.txt" for the `update requirements` workflow in alphashared.
# Use this to resolve cross-os dependency issues.
# For any dependency that is listed before the '-->',
# the part that comes after the '-->' will be appended to the respective line
# in the _requirements.freeze.txt file

# example 1: impose linux-only constraint on nvidia-cublas-cu12 
nvidia-cublas-cu12--> ; sys_platform == 'linux'

# example 2: restrict torch version for darwin-x86_64 only
torch--> ; sys_platform != 'darwin' or platform_machine != 'x86_64'
ADD_DEPENDENCY--> torch==2.2.2; sys_platform == 'darwin' and platform_machine == 'x86_64'
```


## Dockerized version
For local runs, there's a dockerize version: see `Dockerfile` and instructions therein.  