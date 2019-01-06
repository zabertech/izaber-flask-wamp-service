#!/bin/bash

pushd src > /dev/null
python3 run_server.py -c ../osso.yaml
popd > /dev/null
