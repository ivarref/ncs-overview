#!/bin/bash

set -ex

rm -rf data/
rm -rf img/
rm -rf tmp_data/
mkdir data/
mkdir tmp_data/
mkdir img/

./download.sh
./generate.py
./generate_reserves.py
./overview.py > README.md
./screens_from_page.sh ./vis/raudgrøne.js
./screenshots_production.sh
./screenshots_produced_reserves.sh

rm -rf tmp_data/
