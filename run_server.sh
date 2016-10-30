#!/bin/bash

./node_modules/.bin/webpack-dev-server ./vis/entry --hot --inline --module-bind "css=style\!css"