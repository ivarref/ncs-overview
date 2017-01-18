#!/bin/bash

set -ex

[ -d "node_modules" ] || yarn

mkdir -p data/
mkdir -p tmp_data/
mkdir -p img/

if [[ $1 == "--no-download" ]]; then
  echo "not downloading ..."
else
  rm -rf data/*
  rm -rf tmp_data/*
  ./download.sh
  ./download_well.sh
fi

./generate.py
./generate_reserves.py
./add_discovery_year.py
./generate_kumulativ_reservetilvekst_vs_produksjon.py
./calc_wells.py
./split_monthly_production.py
./split_discoveries.py
./split_wellbores.py
./overview.py > README.md
./make_screens.sh

rm -rf tmp_data/
