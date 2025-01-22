#!/bin/bash

# A small command line tool to comment out all alphax lines in a requirements file

set -e

if [ ! "$1" == "" ]; then
  REQUIREMENTS_FILE=$1
else
  # none given -> auto-detect
  if [ -e "requirements.txt" ]; then
    REQUIREMENTS_FILE="requirements.txt"
  elif [ -e "requirements/requirements.txt" ]; then
    REQUIREMENTS_FILE="requirements/requirements.txt"
  elif [ -e "requirements/base.txt" ]; then
    REQUIREMENTS_FILE="requirements/base.txt"
  else
    echo "No requirements file found"
    exit 1
  fi
fi

echo using $REQUIREMENTS_FILE

# Add any alphaX packages that others depend on here. Use the name like it is given in the requirements file!
for a in alphabase alphatims alpharaw peptdeep alphatims alphaviz; do
  sed -i "s/$a/### $a/" $REQUIREMENTS_FILE
done

echo $REQUIREMENTS_FILE:
cat  $REQUIREMENTS_FILE
