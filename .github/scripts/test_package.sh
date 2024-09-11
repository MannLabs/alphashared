#!/bin/bash

test_package() {
  local artifact_name=$1
  local os=$2

  if [ "$os" == "linux" ]; then
    sudo dpkg -i ./${artifact_name}
  elif [ "$os" == "macos" ]; then
    sudo installer -pkg ./${artifact_name} -target /
  else
    ./${artifact_name} //verysilent //SUPPRESSMSGBOXES //log=log.txt //noicons //tasks= //portable=1
    cat log.txt
  fi
}