#!/bin/bash

fswatch -e ".*" -i ".*/[^.]*\\.py$" -i ".*/[^.]*\\.sh$" -i ".*/[^.]*\\.md$" -0 . | xargs -0 -n 1 -I {} ./make.sh
