#!/bin/bash

check_artifact_exists() {
  local artifact_name=$1
  local release_id=$2

  json_response=$(gh api \
    --method GET \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    repos/$GITHUB_REPOSITORY/releases/${release_id}/assets)

  echo $json_response

  if echo "$json_response" | jq -e '.[] | select(.name == "'"${artifact_name}"'")' > /dev/null; then
    echo "Artifact ${artifact_name} already exists in release ${release_id}"
    echo "This might be okay if you are re-running the workflow"
    exit 1
  fi
}