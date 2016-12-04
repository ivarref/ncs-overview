#!/bin/bash

unamestr=`uname`

if [[ "$unamestr" == "Darwin" ]]; then
  fswatch -e ".*" -i ".*/[^.]*\\.py$" -i -i ".*/[^.]*\\.js$" -i ".*/[^.]*\\.sh$" -0 . | xargs -0 -n 1 -I {} ./make.sh $@
else
  while find . -type f -not -path "./.git/*" -not -path "./node_modules/*" -not -name "*.pyc" -not -name "*.png" | inotifywait --fromfile - -e close_write; do clear && ./make.sh $@; done
fi
