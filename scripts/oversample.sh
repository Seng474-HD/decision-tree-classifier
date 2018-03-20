#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Please input the file path"
  exit 1
else
  echo "Running oversampling for $1"
  BALANCE_TYPE="oversample" python $1
fi

