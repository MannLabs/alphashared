#!/bin/bash

get_artifact_name() {
  local package_name=$1
  local version=$2
  local os=$3

  ARCH=$(python -c "import platform; arch=platform.machine().lower(); print('x64' if arch == 'x86_64' else arch)")
  KERNEL=$(python -c "import platform; print(platform.system().lower())")

  BUILD_NAME="${package_name}-${version}-${os}-${KERNEL}-${ARCH}"

  if [ "$os" == "linux" ]; then
    ARTIFACT_NAME="${BUILD_NAME}.deb"
  elif [ "$os" == "macos" ]; then
    ARTIFACT_NAME="${BUILD_NAME}.pkg"
  else
    ARTIFACT_NAME="${BUILD_NAME}.exe"
  fi

  echo "${BUILD_NAME}|${ARTIFACT_NAME}"
}