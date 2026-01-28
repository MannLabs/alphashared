#!/bin/bash

# A small command line tool to comment out all alphax lines in requirements files

set -e

# Find all *requirements*.txt files in current directory and one level deep
FILES=$(find . -maxdepth 2 -name "*requirements*.txt" -type f)

if [ -z "$FILES" ]; then
  echo "No requirements files found"
  exit 1
fi

echo "Found requirements files:"
echo "$FILES"

# Add any alphaX packages that others depend on here. Use the name like it is given in the requirements file!
for axp in alphabase alphatims alpharaw peptdeep alphaviz directlfq alphaquant; do
  for file in $FILES; do
    sed -i "s/$axp/### $axp/" "$file"
  done
done

echo "Modified files:"
for file in $FILES; do
  echo "=== $file ==="
  cat "$file"
done
