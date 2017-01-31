#!/usr/bin/env python3

import collections
import math

import pandas as pd

if __name__=="__main__":
  frame = pd.read_csv('data/raw_wellbore.csv')
  frame = frame[frame["wlbPurpose"] == "WILDCAT"]
  print("number of WILDCAT wellbores:", len(frame))
  areas = frame['wlbMainArea'].unique()

  def process(kind, filename, fn=lambda area, ix, v: v):
    print("*"*80)
    r = collections.OrderedDict()
    reserves = pd.read_csv('data/raw_reserves_field_discovery_year_mboe.csv')
    resources = pd.read_csv('./data/raw_discovery_resources.csv')
    for area in areas:
      f = frame[(frame.wlbMainArea==area) & (frame.wlbEntryYear >= 1900)]
      f = f.sort_values(by='wlbEntryDate')
      cumulative = 0
      res = []
      for (idx, well) in enumerate(f.itertuples(index=False)):
        oil = reserves[reserves.fldName == well.wlbField][kind].sum()
        
        if oil > 0:
          reserves = reserves[reserves.fldName != well.wlbField]

        key = kind.replace('fld', 'dsc').replace('OE', 'Oe')
        oil_resources = resources[resources.dscNpdidDiscovery == well.dscNpdidDiscovery][key].sum()
        if oil_resources > 0 and oil > 0:
          print("unexpected dual match on both reserves and resources", well.dscNpdidDiscovery, well.wlbField)
          sys.exit(1)
        if oil_resources > 0:
          oil_resources = oil_resources * 6.29
          resources = resources[resources.dscNpdidDiscovery != well.dscNpdidDiscovery]

        cumulative += (oil + oil_resources)
        res.append(fn(area, idx, cumulative))
      r[area] = pd.Series(res)
      #r[area+' percentage'] = pd.Series([x*100 / max(res) for x in res])
      print(area, len(f), "wells")
    f = pd.DataFrame(r)
    f.to_csv(filename, index=False, float_format='%.1f')
    return f

  frame_oil = process('fldRecoverableOil', './data/wellbores_cumulative_recoverable_plus_resources_oil_mboe.csv')
  frame_gas = process('fldRecoverableGas', './data/wellbores_cumulative_recoverable_plus_resources_gas_mboe.csv')
  frame_oe = process('fldRecoverableOE', './data/wellbores_cumulative_recoverable_plus_resources_oe_mboe.csv')

  # def make_fn(f):
  #   def p(area, idx, v):
  #     if area == 'North sea':
  #       return v
  #     else:
  #       return (v*100.0) / f['North sea'][idx]
  #   return p

  # process('fldRecoverableOil', './data/wellbores_cumulative_recoverable_plus_resources_oil_relative.csv', make_fn(frame_oil))
  # process('fldRecoverableGas', './data/wellbores_cumulative_recoverable_plus_resources_gas_relative.csv', make_fn(frame_gas))
  # process('fldRecoverableOE', './data/wellbores_cumulative_recoverable_plus_resources_oe_relative.csv', make_fn(frame_oe))

  
  
