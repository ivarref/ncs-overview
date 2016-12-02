#!/bin/bash

while find . -type f -not -path "./.git/*" -not -path "./node_modules/*" -not -name "*.pyc" -not -name "*.png" | inotifywait --fromfile - -e close_write; do clear && ./make.sh $@; done