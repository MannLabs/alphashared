#!/bin/bash

# pip-install the package in the current directory, optionally with an extra.
# pip only warns (exit 0) when an extra is not provided, which silently
# installs less than intended; this turns that case into a hard failure.
# needs to be run in a folder containing a Python package

set -u -e -o pipefail

EXTRA="$1"

if [ -z "$EXTRA" ]; then
    pip install "."
    exit
fi

LOG=$(mktemp)
pip install ".[$EXTRA]" 2>&1 | tee "$LOG"
if grep -q "does not provide the extra" "$LOG"; then
    echo "ERROR: requested extra '$EXTRA' is not provided by this package" >&2
    exit 1
fi
