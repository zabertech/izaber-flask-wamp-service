#!/bin/bash

# Pinched from:
# https://stackoverflow.com/a/246128
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

pushd "$DIR/../src"
git pull --all
npm install
git submodule init
git submodule update
npm run build
popd

if [[ ! -f "$DIR/../osso.yaml" ]] ; then
  pushd $DIR
  python yaml_sample_create.py ../osso.yaml
  popd
fi


