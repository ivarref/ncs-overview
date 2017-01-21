#!/usr/bin/env python3

import csv
import sys

import pandas as pd

import generate

if __name__=="__main__":
  frame = pd.read_csv('./data/raw_reserves_field_discovery_year_mboe.csv')
  frame = frame.sort_values(by=['fldRemainingOil', 'fldDiscoveryYear'], ascending=[False, True])
  frame = frame[frame['fldRemainingOil'] > 0]
  del frame['fldRecoverableOil']
  del frame['fldRecoverableGas']
  del frame['fldRecoverableOE']
  del frame['fldNpdidField']
  del frame['fldRemainingGas']
  del frame['fldRemainingOE']
  frame['cumulativeMboe'] = frame['fldRemainingOil'].cumsum()
  frame['cumulativePercentage'] = 100.0*frame['cumulativeMboe'] / frame['fldRemainingOil'].sum()
  frame.to_csv('./data/remaining_oil.csv', index=False, float_format='%.1f')
  