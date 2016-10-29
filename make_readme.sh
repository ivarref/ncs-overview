#!/bin/bash

cat prefix.md > README.md
echo "" >> README.md
echo "" >> README.md

./overview.py >> README.md
