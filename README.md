# alphashared
Shared non-production code for AlphaX packages

## contents
- `actions`: reusable github actions
- `actions/get-code-review-input`: generates input for AI-assisted code review, see [README](actions/get-code-review-input/README.md)


## Requirements on the caller repository

### create_release.yml
The following files need to be present:
```
if directory release/linux exists:
release/linux/build_backend_linux.sh
release/linux/build_installer_linux.sh
release/linux/build_linux.sh (optional)

if directory release/macos exists:
release/macos/build_backend_macos.sh
release/macos/build_pkg_macos.sh
release/macos/build_gui_macos.sh (optional)

if directory release/windows exists:
release/windows/build_backend.ps1
release/windows/build_installer.ps1
release/windows/build_gui.ps1 (optional)

in <package_name>/__init__.py
__version__ = "<version to release, e.g. 1.2.3>"