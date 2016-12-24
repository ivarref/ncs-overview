#!/bin/bash

set -ex

for fil in $(./eligible_pages.py); do
  ./screens_from_page.sh $fil
done
