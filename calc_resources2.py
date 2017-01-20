#!/usr/bin/env python3

import collections
import json
import os
import sys

import pandas as pd

if __name__=="__main__":
  frame = pd.read_csv('./data/raw_discovery_overview.csv')
  
  resources = pd.read_csv('./data/raw_discovery_resources.csv')
  reserves = pd.read_csv('./data/raw_reserves_field.csv')

  statuses = [status for status in sorted(frame['dscCurrentActivityStatus'].unique())]
  
  def fmt(x):
      return "%.1f" % ((x*6.29))
  
  print("status", "oil_mboe", "gas_mboe", "oe_mboe", sep=",")
  try:
    os.makedirs('./data/resources/')
  except:
    pass

  for status in statuses:
    f = frame[frame['dscCurrentActivityStatus'] == status]
    mask = resources.dscNpdidDiscovery.isin(f.dscNpdidDiscovery)
    oil = resources[mask].dscRecoverableOil.sum()
    gas = resources[mask].dscRecoverableGas.sum()
    oe = resources[mask].dscRecoverableOe.sum()

    mask_reserves = reserves.fldNpdidField.isin(f.fldNpdidField)
    oil_reserves = reserves[mask_reserves].fldRemainingOil.sum()
    gas_reserves = reserves[mask_reserves].fldRemainingGas.sum()
    oe_reserves = reserves[mask_reserves].fldRemainingOE.sum()

    print('"' + status + '"', fmt(oil+oil_reserves), fmt(gas+gas_reserves), fmt(oe+oe_reserves), sep=',')
    fil = './data/resources/%s.json' % (status.replace(",", ""))

    def boe_d_rp_10(x):
      rp = 10.0
      return "%.0f" % ( (1000.0 *6.29*x) / (rp*365.0))
    
    def field_details():
      res = []
      for fldName in reserves[mask_reserves].fldName.unique():
        d = []
        d.append(('discoveryYear', str(reserves[reserves.fldName == fldName].fldDiscoveryYear.values[0])))
        d.append(('oil_mboe', fmt(reserves[reserves.fldName == fldName].fldRemainingOil.sum())))
        d.append(('gas_mboe', fmt(reserves[reserves.fldName == fldName].fldRemainingGas.sum())))
        d.append(('oe_mboe', fmt(reserves[reserves.fldName == fldName].fldRemainingOE.sum())))
        res.append((fldName, collections.OrderedDict(d)))
      return collections.OrderedDict(res)
    
    def discovery_details():
      res = []
      for dscName in resources[mask].dscName.unique():
        d = []
        
        d.append(('discoveryYear', str(resources[resources.dscName == dscName].dscDiscoveryYear.values[0])))
        d.append(('oil_mboe', fmt(resources[resources.dscName == dscName].dscRecoverableOil.sum())))
        d.append(('gas_mboe', fmt(resources[resources.dscName == dscName].dscRecoverableGas.sum())))
        d.append(('oe_mboe', fmt(resources[resources.dscName == dscName].dscRecoverableOe.sum())))
        res.append((dscName, collections.OrderedDict(d)))
      return collections.OrderedDict(res)

    data = [
      ('status', status),
      ('oil_production_kboe_d_rp=10', boe_d_rp_10(oil+oil_reserves)),
      ('gas_production_kboe_d_rp=10', boe_d_rp_10(gas+gas_reserves)),
      ('oe_production_kboe_d_rp=10', boe_d_rp_10(oe+oe_reserves)),
      ('oil_mboe', fmt(oil+oil_reserves)),
      ('gas_mboe', fmt(gas+gas_reserves)),
      ('oe_mboe', fmt(oe+oe_reserves)),
      ('fields', field_details()),
      ('discoveries', discovery_details())
    ]
    
    with open(fil, 'w') as wfd:
      json.dump(collections.OrderedDict(data), wfd, indent=2, ensure_ascii=False)
  oil = reserves.fldRemainingOil.sum() + resources.dscRecoverableOil.sum()
  gas = reserves.fldRemainingGas.sum() + resources.dscRecoverableGas.sum()
  oe = reserves.fldRemainingOE.sum() + resources.dscRecoverableOe.sum()
  print('"Sum"', fmt(oil), fmt(gas), fmt(oe), sep=',')
