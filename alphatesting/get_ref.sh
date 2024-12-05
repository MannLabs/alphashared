#!/bin/bash

# if passed 'latest', return latest tag, otherwise return passed value
# needs to be run in a folder containing a git repository

set -u -e

if [ "$1" == "latest" ]; then
    latestTag=$(git describe --tags "$(git rev-list --tags --max-count=1)")
    echo $latestTag
    exit
fi
echo $1
