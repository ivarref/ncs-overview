#!/usr/bin/env python3

import csv
import sys

import pandas as pd

import generate

if __name__=="__main__":
  frame = pd.read_csv('./data/raw_discovery_overview.csv')

  with open('./data/raw_reserves_field_discovery_year.csv', 'w') as wfd:
    writer = csv.writer(wfd)
    with open('./data/raw_reserves_field_discovery_year_mboe.csv', 'w') as wfd2:
      writer_gboe = csv.writer(wfd2)

      with open('./data/raw_reserves_field.csv', 'r') as rfd:
        reader = csv.reader(rfd)
        for (idx, row) in enumerate(reader):
          if idx==0:
            if row[0] != 'fldName':
              print("format changed, expected fldName for first column, was", row[0])
              sys.exit(1)
            header = [row[0], 'fldDiscoveryYear', 'fldCurrentActivityStatus'] + row[1:]
            writer.writerow(header)
            writer_gboe.writerow(header)
          else:
            fldName = row[0]
            f = frame[frame['fldName'] == fldName]
            years = f['dscDiscoveryYear'].unique()
            dscCurrentActivityStatus = f['dscCurrentActivityStatus'].unique()
            if len(years) != 1 or len(dscCurrentActivityStatus) != 1:
              print("expected a single year, got", len(years), "for field", fldName)
              sys.exit(1)
            writer.writerow([row[0], years[0], dscCurrentActivityStatus[0]] + row[1:])
            def to_gboe(items):
              return ["%.1f" % (float(x)*6.29) for x in items]
            writer_gboe.writerow([row[0], years[0], dscCurrentActivityStatus[0]] + to_gboe(row[1:-1]) + [row[-1]])
