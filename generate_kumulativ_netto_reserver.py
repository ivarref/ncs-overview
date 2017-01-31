#!/usr/bin/env python3

import csv
import os
import sys

import pandas as pd

import generate


if __name__=="__main__":
  production = pd.read_csv('./data/raw_production_yearly_field.csv')
  reserves = pd.read_csv('./data/raw_reserves_field_discovery_year.csv')

  start_year = reserves.fldDiscoveryYear.min()
  stop_year = max(production.prfYear.max(), reserves.fldDiscoveryYear.max())
  
  decade_to_fields = generate.get_decade_to_fields(generate.get_discovery_years(reserves.fldName.unique()))
  
  res = []
  years = range(start_year, stop_year+1)
  for year in years:
    r = []
    for (decade, fields) in decade_to_fields.items():
      cumulative_reserves = reserves[(reserves.fldDiscoveryYear <= year)  & reserves.fldName.isin(fields)]['fldRecoverableOil'].sum()
      cumulative_produced = production[(production.prfYear <= year)  & production.prfInformationCarrier.isin(fields)]['prfPrdOilNetMillSm3'].sum()
      mboe = 6.29*(cumulative_reserves - cumulative_produced)
      r.append(mboe)
    res.append([year] + r + [sum(r)])
  frame = pd.DataFrame(res, columns=['year'] + list(decade_to_fields.keys()) + ['Sum'])
  frame.to_csv('./data/cumulative net reserves oil mboe.csv', index=False, float_format="%.1f")
  