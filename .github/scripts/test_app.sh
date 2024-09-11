#!/bin/bash

test_app() {
  local package_name=$1
  local os=$2

  if [ "$os" == "windows" ]; then
    EXECUTABLE="dist_pyinstaller/${package_name}/${package_name}.exe"
  else
    EXECUTABLE="dist_pyinstaller/${package_name}/${package_name}"
  fi
  COMMAND="--version"

  if [ ! -e ${EXECUTABLE} ]; then
    if [ "$os" == "windows" ]; then
      EXECUTABLE="dist_pyinstaller/${package_name}_gui/${package_name}_gui.exe"
    else
      EXECUTABLE="dist_pyinstaller/${package_name}_gui/${package_name}_gui"
    fi
    COMMAND="--help"
  fi

  echo "calling ${EXECUTABLE} ${COMMAND}"
  eval ${EXECUTABLE} ${COMMAND}
}