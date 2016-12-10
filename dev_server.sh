#!/bin/bash

#./node_modules/.bin/webpack-dev-server ./vis/entry --hot --inline --module-bind "css=style\!css"
./node_modules/.bin/webpack-dev-server $1 --hot --inline --module-bind "css=style\!css"