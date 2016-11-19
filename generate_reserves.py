#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import csv

import pandas as pd

import generate


def get_distinct_fields():
  frame = pd.read_csv('./data/raw_reserves_field.csv')
  ids = frame[u'fldNpdidField'].unique()
  return ids

def remaining_reserve(field_id, kind):
  frame = pd.read_csv('./data/raw_reserves_field.csv')
  f = frame[frame[u'fldNpdidField'] == field_id]
  return f[kind].values[0]

if __name__=="__main__":
    # get distinct field ids
    ids = get_distinct_fields()

    # get discovery year for each id
    id_to_year = generate.get_discovery_years(ids)

    # group fields by discovery decade
    decade_to_fields = generate.get_decade_to_fields(id_to_year)
    decades = decade_to_fields.keys()
    decades.sort()
    print("reserves")
    print("-"*80)
    for decade in decades:
        remaining_oil = sum([remaining_reserve(field_id, 'fldRemainingOil') for field_id in decade_to_fields[decade]])
        remaining_gas = sum([remaining_reserve(field_id, 'fldRemainingGas') for field_id in decade_to_fields[decade]])
        remaining_oe = sum([remaining_reserve(field_id, 'fldRemainingOE') for field_id in decade_to_fields[decade]])
        print(decade, remaining_oil, remaining_gas, remaining_oe)
    print("-"*80)

    