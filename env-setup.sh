#!/bin/bash

pushd src
git pull --all
npm install
git submodule init
git submodule update
npm run build
popd

if [[ ! -f osso.yaml ]] ; then
  cp osso.yaml.sample osso.yaml
fi

