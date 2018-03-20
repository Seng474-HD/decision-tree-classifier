#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Please input the file path"
  exit 1
else
  echo "Running undersampling for $1"
  BALANCE_TYPE="undersample" python $1
fi

