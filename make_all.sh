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
./docker_screenshots.sh

rm -rf tmp_data/
