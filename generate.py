#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import csv
import inspect
import json
import os
import sys

import pandas as pd


def npdid_name(id):
  frame = pd.read_csv('./data/raw_production_monthly_field.csv')
  f = frame[frame[u'prfNpdidInformationCarrier'] == id]
  return f['prfInformationCarrier'].values[0]

def get_distinct_fields():
  frame = pd.read_csv('./data/raw_production_monthly_field.csv')
  ids = frame[u'prfInformationCarrier'].unique()
  return sorted(ids)

def get_production_years(ids):
  frame = pd.read_csv('./data/raw_production_monthly_field.csv')
  res = []
  before = 'Før 2000'
  after = 'Etter 2000'
  d = collections.OrderedDict()
  d[before] = []
  d[after] = []
  for (idx, id) in enumerate(ids):
    m = frame[frame['prfInformationCarrier'] == id]
    year = m['prfYear'].min()
    if year < 2000:
      yr = before
    else:
      yr = after
    d[yr].append(id)
  return d

def get_giant_status(ids, prop):
  frame = pd.read_csv('./data/raw_reserves_field_discovery_year_mboe.csv')
  res = []
  before = 'Gigant'
  after = 'Ikkje gigant'
  d = collections.OrderedDict()
  d[before] = []
  d[after] = []
  for (idx, id) in enumerate(ids):
    m = frame[frame['fldName'] == id]
    kind = m[prop].min()
    if kind >= 1000:
      kind = before
    else:
      kind = after
    d[kind].append(id)
  return d


def get_discovery_years(ids):
  frame = pd.read_csv('./data/raw_discovery_overview_simplified.csv')
  res = []
  for (idx, id) in enumerate(ids):
    m = frame[frame['fldName'] == id]
    years = m['dscDiscoveryYear'].unique()
    if len(years) != 1:
      print("%s:%d get_discovery_years error: npdid" % (__file__, inspect.stack()[0][2]), id, npdid_name(id), "with", len(years), "matches", years)
      sys.exit(1)
    year = min(years)
    res.append((id, year))
  return collections.OrderedDict(res)

def get_discovery_region_to_fields(ids):
  frame = pd.read_csv('./data/raw_discovery_overview_simplified.csv')
  d = collections.defaultdict(list)
  for (idx, id) in enumerate(ids):
    m = frame[frame['fldName'] == id]
    region = m['nmaName'].unique()
    if len(region) != 1:
      print("%s:%d get_discovery_region_name error: npdid" % (__file__, inspect.stack()[0][2]), id, npdid_name(id), "with", len(region), "matches", region)
      sys.exit(1)
    d[region[0]].append(id)
  
  order = ['North sea', 'Norwegian sea', 'Barents sea']
  r = collections.OrderedDict()
  for k in d.keys():
    if k not in order:
      print("%s:%d did not find key" % (__file__, inspect.stack()[0][2]), k)
      sys.exit(1)
  for k in order:
    r[k] = d[k]
  return r

def get_decade_to_fields(id_to_year):
  decade_to_fields = collections.defaultdict(list)
  decade_of_year = lambda x: str(x - (x%10))
  for (id, year) in id_to_year.items():
    decade_to_fields[decade_of_year(year)].append(id)
  return collections.OrderedDict(sorted([(k, sorted(v)) for (k,v) in decade_to_fields.items()]))

def write_file_for_property(group_to_ids, filename, prop, monthly=False, process = lambda y, x: x, should_write = lambda y: True):
  # get all production dates
  df = pd.read_csv('./data/raw_production_monthly_field.csv')
  df['prfMonthStr'] = df['prfMonth'].astype(str)
  mask = df['prfMonthStr'].str.len() == 1
  df.loc[mask, 'prfMonthStr'] = '0' + df['prfMonthStr']
  df['prfYearMonth'] = df['prfYear'].astype(str) + '-' + df['prfMonthStr']
  alldates = df['prfYearMonth'].unique()
  alldates.sort()

  prevdates = []
  print('writing file', filename)
  with open(filename, 'w') as csvfile:
    writer = csv.writer(csvfile)
    header = ['Date']
    header.extend(group_to_ids.keys())
    header.append('Sum')
    writer.writerow(header)
    
    started_writing = False

    for date in alldates:
      prevdates.append(date)
      yr = date.split("-")[0]
      year = int(date.split("-")[0])
      month = date.split("-")[1]
      lastrow = date == alldates[-1]
      endofyear = month=="12"
      if len(prevdates) != 12:
        continue
      elif endofyear or lastrow or monthly:
        if monthly:
          yr = date
        row = [yr]
        for (group, group_fields) in group_to_ids.items():
          months = df[df['prfYearMonth'].isin(prevdates)]
          fields = months[months['prfInformationCarrier'].isin(group_fields)]
          v = process(year, fields[prop].sum())
          row.append("%g" % (v))
          #print(date, prop, group, v)
        
        months = df[df['prfYearMonth'].isin(prevdates)]
        sum = process(year, months[prop].sum())
        row.append("%g" % (sum))
        if sum == 0 and started_writing == False:
          pass
        else:
          started_writing = True
          writer.writerow(row)
      prevdates.remove(prevdates[0])

def is_leap(year):
  return ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0)

def to_mboe_d(year, x):
  # http://www.npd.no/no/Nyheter/Produksjonstall/2016/Juli-2016/
  # 1 Sm3 olje ≈ 6,29 fat
  barrels = x*6.29
  days = 365.0
  if is_leap(year):
    days = 366.0
  return barrels / days

def generate_decade():
  try:
    os.makedirs('data/decade')
  except:
    pass

  # get distinct field ids
  ids = get_distinct_fields()
  print("number of distinct field ids", len(ids))

  # get discovery year for each id
  id_to_year = get_discovery_years(ids)

  # group fields by discovery decade
  decade_to_fields = get_decade_to_fields(id_to_year)
  with open('./data/decade_to_fields_production.json', 'w') as wfd:
    json.dump(decade_to_fields, wfd, sort_keys=True, indent=2, ensure_ascii=False)

  write_file_for_property(decade_to_fields, 'data/decade/oil_production_yearly_12MMA_MillSm3_by_discovery_decade.csv', 'prfPrdOilNetMillSm3')
  write_file_for_property(decade_to_fields, 'data/decade/gas_production_yearly_12MMA_BillSm3_by_discovery_decade.csv', 'prfPrdGasNetBillSm3')
  write_file_for_property(decade_to_fields, 'data/decade/oe_production_yearly_12MMA_MillSm3_by_discovery_decade.csv', 'prfPrdOeNetMillSm3')

  write_file_for_property(decade_to_fields, 'data/decade/oil_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdOilNetMillSm3', monthly=True, process=to_mboe_d)
  write_file_for_property(decade_to_fields, 'data/decade/gas_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdGasNetBillSm3', monthly=True, process=to_mboe_d)
  write_file_for_property(decade_to_fields, 'data/decade/oe_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdOeNetMillSm3', monthly=True, process=to_mboe_d)

  write_file_for_property(decade_to_fields, 'data/decade/oil_production_yearly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdOilNetMillSm3', monthly=False, process=to_mboe_d)
  write_file_for_property(decade_to_fields, 'data/decade/gas_production_yearly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdGasNetBillSm3', monthly=False, process=to_mboe_d)
  write_file_for_property(decade_to_fields, 'data/decade/oe_production_yearly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdOeNetMillSm3', monthly=False, process=to_mboe_d)

def generate_region():
  region_to_fields = get_discovery_region_to_fields(get_distinct_fields())
  with open('./data/region_to_fields_production.json', 'w') as wfd:
    json.dump(region_to_fields, wfd, sort_keys=True, indent=2, ensure_ascii=False)

  try:
    os.makedirs('data/region')
  except:
    pass
  write_file_for_property(region_to_fields, 'data/region/oil_production_yearly_12MMA_MillSm3_by_region.csv', 'prfPrdOilNetMillSm3')
  write_file_for_property(region_to_fields, 'data/region/gas_production_yearly_12MMA_BillSm3_by_region.csv', 'prfPrdGasNetBillSm3')
  write_file_for_property(region_to_fields, 'data/region/oe_production_yearly_12MMA_MillSm3_by_region.csv', 'prfPrdOeNetMillSm3')

  write_file_for_property(region_to_fields, 'data/region/oil_production_monthly_12MMA_mboe_d_by_region.csv', 'prfPrdOilNetMillSm3', monthly=True, process=to_mboe_d)
  write_file_for_property(region_to_fields, 'data/region/gas_production_monthly_12MMA_mboe_d_by_region.csv', 'prfPrdGasNetBillSm3', monthly=True, process=to_mboe_d)
  write_file_for_property(region_to_fields, 'data/region/oe_production_monthly_12MMA_mboe_d_by_region.csv', 'prfPrdOeNetMillSm3', monthly=True, process=to_mboe_d)

  write_file_for_property(region_to_fields, 'data/region/oil_production_yearly_12MMA_mboe_d_by_region.csv', 'prfPrdOilNetMillSm3', monthly=False, process=to_mboe_d)
  write_file_for_property(region_to_fields, 'data/region/gas_production_yearly_12MMA_mboe_d_by_region.csv', 'prfPrdGasNetBillSm3', monthly=False, process=to_mboe_d)
  write_file_for_property(region_to_fields, 'data/region/oe_production_yearly_12MMA_mboe_d_by_region.csv', 'prfPrdOeNetMillSm3', monthly=False, process=to_mboe_d)

def generate_millennium():
  millennium_to_fields = get_production_years(get_distinct_fields())
  try:
    os.makedirs('data/millennium')
  except:
    pass
  write_file_for_property(millennium_to_fields, 'data/millennium/oil_production_yearly_12MMA_mboe_d_by_startproduction.csv', 'prfPrdOilNetMillSm3', monthly=False, process=to_mboe_d, should_write=lambda y: y>=2000)
  write_file_for_property(millennium_to_fields, 'data/millennium/gas_production_yearly_12MMA_mboe_d_by_startproduction.csv', 'prfPrdGasNetBillSm3', monthly=False, process=to_mboe_d, should_write=lambda y: y>=2000)
  write_file_for_property(millennium_to_fields, 'data/millennium/oe_production_yearly_12MMA_mboe_d_by_startproduction.csv', 'prfPrdOeNetMillSm3', monthly=False, process=to_mboe_d, should_write=lambda y: y>=2000)

def generate_giants():
  try:
    os.makedirs('data/giants')
  except:
    pass
  write_file_for_property(get_giant_status(get_distinct_fields(), 'fldRecoverableOil'), 'data/giants/oil_production_yearly_12MMA_mboe_d_by_fieldsize.csv', 'prfPrdOilNetMillSm3', monthly=False, process=to_mboe_d)
  write_file_for_property(get_giant_status(get_distinct_fields(), 'fldRecoverableGas'), 'data/giants/gas_production_yearly_12MMA_mboe_d_by_fieldsize.csv', 'prfPrdGasNetBillSm3', monthly=False, process=to_mboe_d)
  write_file_for_property(get_giant_status(get_distinct_fields(), 'fldRecoverableOE'), 'data/giants/oe_production_yearly_12MMA_mboe_d_by_fieldsize.csv', 'prfPrdOeNetMillSm3', monthly=False, process=to_mboe_d)
  
if __name__=="__main__":
  print("start generate.py ...")
  generate_decade()
  generate_region()
  generate_millennium()
  generate_giants()

  print("exiting generate.py ...")
