#!/bin/bash

set -ex

rm -rf data/
rm -rf tmp_data/
mkdir data/
mkdir tmp_data/

./download.sh
./generate.py
./generate_reserves.py
./overview.py > README.md

# create those screenshots....
rm -rf img/
mkdir img
./node_modules/.bin/webpack-dev-server ./vis/entry --hot --inline --module-bind "css=style\!css" &
SERVER_PID=$!
sleep 5 # such hack...
echo "starting to take screenshots ..."
./screenshots.py
kill $SERVER_PID

rm -rf tmp_data/
