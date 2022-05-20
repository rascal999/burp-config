#!/usr/bin/env bash

CURRENT_DIR=`pwd | gawk -F '/' '{ print $NF }'`

if [[ "$CURRENT_DIR" != "burp-config" ]]; then
  echo "ERROR: Must run from burp-config directory"
  exit 1
fi

if [[ "$#" -ne "1" ]]; then
  echo "ERROR: Specify commit message, or double quote"
  exit 1
fi

echo "Copying from ~/.BurpSuite .."
cp -rf ~/.BurpSuite .
echo "git add'ing .."
git add .
echo "Committing .."
git commit -m "$1"
echo "Pushing .."
git push
