# alphashared
Shared non-production code for AlphaX packages

## contents
- `actions`: reusable github actions
- `actions/get-code-review-input`: generates input for AI-assisted code review, see [README](actions/get-code-review-input/README.md)

## Requirements on the caller repository

### create_release.yml
The following files need to be present:
```
release/macos/build_backend_macos.sh
release/macos/build_pkg_macos.sh
release/macos/build_gui_macos.sh (optional)

release/windows/build_backend.ps1
release/windows/build_installer.ps1
release/windows/build_gui.ps1 (optional)
```
