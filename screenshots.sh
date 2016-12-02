#!/bin/bash
set -ex

# create those screenshots....
rm -rf img/
mkdir img
./node_modules/.bin/webpack-dev-server ./vis/entry --hot --inline --module-bind "css=style\!css" &
SERVER_PID=$!
sleep 5 # such hack...
echo "starting to take screenshots ..."
./screenshots.py
kill $SERVER_PID
