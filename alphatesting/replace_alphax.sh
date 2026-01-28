#!/bin/bash

# A small command line tool to comment out all alphax lines in requirements and pyproject.toml files

set -e

# Find all *requirements*.txt files in current directory and one level deep
REQ_FILES=$(find . -maxdepth 2 -name "*requirements*.txt" -type f)

# Find all pyproject.toml files in current directory and one level deep
TOML_FILES=$(find . -maxdepth 2 -name "pyproject.toml" -type f)

if [ -z "$REQ_FILES" ] && [ -z "$TOML_FILES" ]; then
  echo "No requirements or pyproject.toml files found"
  exit 1
fi

echo "Found requirements files:"
echo "$REQ_FILES"
echo "Found pyproject.toml files:"
echo "$TOML_FILES"

# Add any alphaX packages that others depend on here. Use the name like it is given in the requirements file!
for axp in alphabase alphatims alpharaw peptdeep alphaviz directlfq alphaquant; do
  for file in $REQ_FILES; do
    sed -i "s/$axp/### $axp/" "$file"
  done
  for file in $TOML_FILES; do
    # Comment out entire lines containing the package in pyproject.toml
    # Note: this assumes each package is on its own line and uses double quotes
    sed -i "s/^\\([[:space:]]*\\)\"$axp/\\1# \"$axp/" "$file"
  done
done

echo "Modified files:"
for file in $REQ_FILES $TOML_FILES; do
  echo "=== $file ==="
  cat "$file"
done
