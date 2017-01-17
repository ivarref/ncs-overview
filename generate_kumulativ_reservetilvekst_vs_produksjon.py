#!/usr/bin/env python3

import collections
import csv
import datetime
import json
import os
import sys

import pandas as pd

import generate
import generate_reserves


def recoverable(field_id, kind):
  frame = pd.read_csv('./data/raw_reserves_field.csv')
  f = frame[frame[u'fldName'] == field_id]
  return f[kind].values[0]

def cumulative_recoverable_since(since_year):
  field_to_year = generate.get_discovery_years(generate_reserves.get_distinct_fields())
  sidan_x = collections.OrderedDict([(field, str(year)) for (field, year) in field_to_year.items() if year >= since_year])
  with open('./data/discoveries_since_%d.json' % (since_year), 'w') as wfd:
    json.dump(sidan_x, wfd, indent=2, ensure_ascii=False)
  
  result = []
  for year in range(since_year, datetime.datetime.now().year+1):
    fields = [field for (field, yr) in sidan_x.items() if yr <= str(year)]
    recoverableOil = sum([recoverable(field, 'fldRecoverableOil') for field in fields])
    recoverableGas = sum([recoverable(field, 'fldRecoverableGas') for field in fields])
    recoverableOE = sum([recoverable(field, 'fldRecoverableOE') for field in fields])
    # fldRecoverableOil,fldRecoverableGas,fldRecoverableOE
    result.append((year, recoverableOil, recoverableGas, recoverableOE))
  return result

def cumulative_produced_since(since_year):
  frame = pd.read_csv('./data/raw_production_yearly_total.csv')
  frame = frame[frame['prfYear'] >= since_year]
  result = []
  for year in range(since_year, datetime.datetime.now().year+1):
    prfPrdOilNetMillSm3 = frame[frame['prfYear'] <= year]['prfPrdOilNetMillSm3'].sum()
    prfPrdGasNetBillSm3 = frame[frame['prfYear'] <= year]['prfPrdGasNetBillSm3'].sum()
    prfPrdOeNetMillSm3  = frame[frame['prfYear'] <= year]['prfPrdOeNetMillSm3'].sum()
    result.append((year, prfPrdOilNetMillSm3, prfPrdGasNetBillSm3, prfPrdOeNetMillSm3))
  return result

if __name__=="__main__":
  def fmt(x):
    return "%.2f" % (x*6.29 / 1000.0)

  def process_year(year):
    recoverable = cumulative_recoverable_since(year)
    produced = cumulative_produced_since(year)

    try:
      os.makedirs('./data/cumulative/')
    except:
      pass
    filename = './data/cumulative/cumulative_reserves_vs_production_since_%d_gboe.csv' % (year)
    if os.path.exists(filename):
      os.remove(filename)

    with open(filename, 'w') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(['year', 'reserveOil', 'reserveGas', 'reserveOE', 'producedOil', 'producedGas', 'producedOE'])

      for ((reserve_year,reserve_oil, reserve_gas, reserve_oe), (prod_year, prod_oil, prod_gas, prod_oe)) in zip(recoverable, produced):
        if prod_year != reserve_year:
          print("uh oh! Got prod year", prod_year, "and reserve_year", reserve_year)
          sys.exit(1)
        writer.writerow([reserve_year, fmt(reserve_oil), fmt(reserve_gas), fmt(reserve_oe), fmt(prod_oil), fmt(prod_gas), fmt(prod_oe)])

  process_year(2000)