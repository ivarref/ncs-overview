#!/bin/bash

set -ex

./download.sh
./generate.py
./make_readme.sh
