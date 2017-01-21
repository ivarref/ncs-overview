#!/usr/bin/env python3

import csv
import sys

import pandas as pd

import generate

if __name__=="__main__":
  def produce(fld, filename):
    frame = pd.read_csv('./data/raw_reserves_field_discovery_year_mboe.csv')
    frame = frame.sort_values(by=[fld, 'fldDiscoveryYear'], ascending=[False, True])
    frame = frame[frame[fld] > 0]
    del frame['fldRecoverableOil']
    del frame['fldRecoverableGas']
    del frame['fldRecoverableOE']
    del frame['fldNpdidField']
    for f in ['fldRemainingGas', 'fldRemainingOil', 'fldRemainingOE']:
      if f == fld:
        continue
      del frame[f]
    frame['cumulativeMboe'] = frame[fld].cumsum()
    frame['cumulativePercentage'] = 100.0*frame['cumulativeMboe'] / frame[fld].sum()
    frame.to_csv('./data/%s' % filename, index=False, float_format='%.1f')
  produce('fldRemainingOil', 'remaining_oil_mboe.csv')
  produce('fldRemainingGas', 'remaining_gas_mboe.csv')
  produce('fldRemainingOE', 'remaining_oe_mboe.csv')