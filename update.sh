#!/usr/bin/env bash

CURRENT_DIR=`pwd | gawk -F '/' '{ print $NF }'`

if [[ "$CURRENT_DIR" != "burp-config" ]]; then
  echo "ERROR: Must run from burp-config directory"
  exit 1
fi

git pull
mv ~/.BurpSuite/ ~/.BurpSuite-`date +"%Y%m%d_%H%M%S"`
cp -rf .BurpSuite ~/
