#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import collections
import csv

import pandas as pd


def npdid_name(id):
  frame = pd.read_csv('./data/raw_production_monthly_field.csv')
  f = frame[frame[u'prfNpdidInformationCarrier'] == id]
  return f['prfInformationCarrier'].values[0]

def get_distinct_fields():
  frame = pd.read_csv('./data/raw_production_monthly_field.csv')
  ids = frame[u'prfNpdidInformationCarrier'].unique()
  return ids

def get_discovery_years(ids):
  frame = pd.read_csv('./data/raw_discovery_overview.csv')
  frame = frame[frame['dscCurrentActivityStatus'] != 'INCLUDED IN OTHER DISCOVERY']
  res = []
  for (idx, id) in enumerate(ids):
    m = frame[frame['fldNpdidField'] == id]
    years = m['dscDiscoveryYear'].unique()
    # Likvern:
    # Om jeg husker riktig så pågår det ”prøveproduksjon” fra ”Delta 33/9-6". Funnet ble gjort i 1976 er nå formelt vedtatt utbygd og estimert utvinnbart er rundt 0,074 millioner Sm3 (0,47 millioner fat) olje.
    #if len(years) == 0 and npdid_name(id) == "33/9-6 DELTA":
    #  years = [1976]
      
    if len(years) != 1:
      print("warning: npdid", id, npdid_name(id), "with", len(years), "matches", years)

    year = min(years)
    res.append((id, year))
  return dict(res)

def get_decade_to_fields(id_to_year):
  decade_to_fields = {}
  decade_of_year = lambda x: x - (x%10)
  for (id, year) in id_to_year.items():
    decade = decade_of_year(year)
    if decade not in decade_to_fields:
      decade_to_fields[decade] = []
    decade_to_fields[decade].append(id)
  return collections.OrderedDict(sorted(decade_to_fields.items()))

if __name__=="__main__":
  print("start generate.py ...")
  
  # get distinct field ids
  ids = get_distinct_fields()
  print("number of distinct field ids", len(ids))

  # get discovery year for each id
  id_to_year = get_discovery_years(ids)

  # group fields by discovery decade
  decade_to_fields = get_decade_to_fields(id_to_year)

  # get all production dates
  df = pd.read_csv('./data/raw_production_monthly_field.csv')
  df['prfMonthStr'] = df['prfMonth'].astype(str)
  mask = df['prfMonthStr'].str.len() == 1
  df.loc[mask, 'prfMonthStr'] = '0' + df['prfMonthStr']
  df['prfYearMonth'] = df['prfYear'].astype(str) + '-' + df['prfMonthStr']
  alldates = df['prfYearMonth'].unique()
  alldates.sort()
  
  decades = decade_to_fields.keys()
  decades.sort()

  def write_file_for_property(filename, prop, monthly=False, process = lambda y, x: x):
    prevdates = []
    with open(filename, 'wb') as csvfile:
      writer = csv.writer(csvfile)
      header = ['Date']
      header.extend(decades)
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
          for decade in decades:
            months = df[df['prfYearMonth'].isin(prevdates)]
            fields = months[months['prfNpdidInformationCarrier'].isin(decade_to_fields[decade])]
            v = process(year, fields[prop].sum())
            row.append("%g" % (v))
            print(date, prop, decade, v)
          
          months = df[df['prfYearMonth'].isin(prevdates)]
          sum = process(year, months[prop].sum())
          row.append("%g" % (sum))
          if sum == 0 and started_writing == False:
            pass
          else:
            started_writing = True
            writer.writerow(row)
        prevdates.remove(prevdates[0])
  
  write_file_for_property('data/oil_production_yearly_12MMA_MillSm3_by_discovery_decade.csv', 'prfPrdOilNetMillSm3')
  write_file_for_property('data/gas_production_yearly_12MMA_BillSm3_by_discovery_decade.csv', 'prfPrdGasNetBillSm3')
  write_file_for_property('data/oe_production_yearly_12MMA_MillSm3_by_discovery_decade.csv', 'prfPrdOeNetMillSm3')
  
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
  write_file_for_property('data/oil_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdOilNetMillSm3', monthly=True, process=to_mboe_d)
  write_file_for_property('data/gas_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdGasNetBillSm3', monthly=True, process=to_mboe_d)
  write_file_for_property('data/oe_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdOeNetMillSm3', monthly=True, process=to_mboe_d)

  write_file_for_property('data/oil_production_yearly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdOilNetMillSm3', monthly=False, process=to_mboe_d)
  write_file_for_property('data/gas_production_yearly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdGasNetBillSm3', monthly=False, process=to_mboe_d)
  write_file_for_property('data/oe_production_yearly_12MMA_mboe_d_by_discovery_decade.csv', 'prfPrdOeNetMillSm3', monthly=False, process=to_mboe_d)
  
  print("exiting generate.py ...")
