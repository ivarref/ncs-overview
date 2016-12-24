#!/bin/bash

set -ex

mkdir -p data/
mkdir -p tmp_data/
mkdir -p img/

if [[ $1 == "--no-download" ]]; then
  echo "not downloading ..."
else
  rm -rf data/*
  rm -rf tmp_data/*
  ./download.sh
fi

./generate.py
./generate_reserves.py
./split_monthly_production.py
./split_discoveries.py
./overview.py > README.md
./make_screens.sh

rm -rf tmp_data/
