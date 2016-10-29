#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import csv
import datetime
import itertools

import pandas as pd


def npdid_name(id):
  frame = pd.read_csv('./raw_production_monthly_field.csv')
  f = frame[frame[u'prfNpdidInformationCarrier'] == id]
  return f['prfInformationCarrier'].values[0]

def get_distinct_fields():
  frame = pd.read_csv('./raw_production_monthly_field.csv')
  ids = frame[u'prfNpdidInformationCarrier'].unique()
  return ids

def get_discovery_years(ids):
  frame = pd.read_csv('./raw_discovery_overview.csv')
  frame = frame[frame['dscCurrentActivityStatus'] != 'INCLUDED IN OTHER DISCOVERY']
  res = []
  for (idx, id) in enumerate(ids):
    m = frame[frame['fldNpdidField'] == id]
    years = m['dscDiscoveryYear'].unique()
    # Likvern:
    # Om jeg husker riktig så pågår det ”prøveproduksjon” fra ”Delta 33/9-6". Funnet ble gjort i 1976 er nå formelt vedtatt utbygd og estimert utvinnbart er rundt 0,074 millioner Sm3 (0,47 millioner fat) olje.
    if len(years) == 0 and npdid_name(id) == "33/9-6 DELTA":
      years = [1976]
    
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
  return decade_to_fields

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
  df = pd.read_csv('./raw_production_monthly_field.csv')
  df['prfMonthStr'] = df['prfMonth'].astype(str)
  mask = df['prfMonthStr'].str.len() == 1
  df.loc[mask, 'prfMonthStr'] = '0' + df['prfMonthStr']
  df['prfYearMonth'] = df['prfYear'].astype(str) + '-' + df['prfMonthStr']
  alldates = df['prfYearMonth'].unique()
  alldates.sort()
  
  prevdates = []
  decades = decade_to_fields.keys()
  decades.sort()

  #props = ['prfPrdOilNetMillSm3', 'prfPrdGasNetBillSm3', 'prfPrdOeNetMillSm3']
  
  now = datetime.datetime.now()

  def write_file_for_property(filename, prop):
    with open(filename, 'wb') as csvfile:
      writer = csv.writer(csvfile)
      header = ['date']
      header.extend(decades)
      writer.writerow(header)

      for date in alldates:
        prevdates.append(date)
        yr = date.split("-")[0]
        month = date.split("-")[1]
        if len(prevdates) == 12 and (month=="12" or date == alldates[-1]):
          if month!="12":
            yr+="-YTD"
          row = [yr]
          for decade in decades:
            months = df[df['prfYearMonth'].isin(prevdates)]
            fields = months[months['prfNpdidInformationCarrier'].isin(decade_to_fields[decade])]
            row.append("%g" % (fields[prop].sum()))
            print(date, prop, decade, fields[prop].sum())
          writer.writerow(row)
          prevdates.remove(prevdates[0])
        elif len(prevdates) == 12:
          prevdates.remove(prevdates[0])
  
  write_file_for_property('oil_production_by_discovery_decade.csv', 'prfPrdOilNetMillSm3')

  print("exiting generate.py ...")
