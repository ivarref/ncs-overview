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
./split_monthly_production.py
./split_discoveries.py
./overview.py > README.md
./make_screens.sh

rm -rf tmp_data/
