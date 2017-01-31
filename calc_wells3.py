#!/usr/bin/env python3

import collections

import pandas as pd

if __name__=="__main__":

  def process_region(region):
    print("*"*80)
    frame = pd.read_csv('./data/raw_discovery_overview.csv')
    frame = frame[frame.nmaName == region]
    frame = frame[frame.dscCurrentActivityStatus != 'Production is unlikely']
    resources = pd.read_csv('./data/raw_discovery_resources.csv')
    reserves = pd.read_csv('./data/raw_reserves_field.csv')

    def get_row(dscName, dscDiscoveryYear, dscCurrentActivityStatus, list_dscNpdidDiscovery, list_fldNpdidField):
      mask = resources.dscNpdidDiscovery.isin(list_dscNpdidDiscovery)
      oil_resources = resources[mask].dscRecoverableOil.sum()
      gas_resources = resources[mask].dscRecoverableGas.sum()
      oe_resources = resources[mask].dscRecoverableOe.sum()

      mask_reserves = reserves.fldNpdidField.isin(list_fldNpdidField)
      oil_reserves = reserves[mask_reserves].fldRemainingOil.sum()
      gas_reserves = reserves[mask_reserves].fldRemainingGas.sum()
      oe_reserves = reserves[mask_reserves].fldRemainingOE.sum()

      kind = ""
      if oe_resources > 0:
        kind = 'resource'
      elif oe_reserves > 0:
        kind = 'reserve'
      else:
        kind = 'unknown'
      row = [
        dscName,
        kind,
        dscDiscoveryYear,
        dscCurrentActivityStatus,
        6.29*(oil_resources+oil_reserves),
        6.29*(gas_resources+gas_reserves),
        6.29*(oe_resources+oe_reserves)
      ]
      return row
    res = []
    for f in frame.itertuples():
      dscName = f.dscName
      dscDiscoveryYear = f.dscDiscoveryYear
      res.append(get_row(dscName, dscDiscoveryYear, f.dscCurrentActivityStatus, [f.dscNpdidDiscovery], [f.fldNpdidField]))

    columns=['dscName', 'kind', 'dscDiscoveryYear', 'dscCurrentActivityStatus', 'oil', 'gas', 'oe']
    f = pd.DataFrame(res, columns=columns)
    f = f.sort_values(by=['oe'], ascending=[False])

    resource = f[f.kind=='resource']
    reserve = f[f.kind=='reserve']
    f = f.append(pd.DataFrame([
      ['Sum resources', 'resource', 'All', 'Any', resource.oil.sum(), resource.gas.sum(), resource.oe.sum()],
      ['Sum reserves', 'reserve', 'All', 'Any', reserve.oil.sum(), reserve.gas.sum(), reserve.oe.sum()],
      get_row('Sum', 'All', 'All', frame.dscNpdidDiscovery, frame.fldNpdidField)
      ], columns=columns))
    f.to_csv('./data/region/resources_reserves %s mboe.csv' % (region), index=False, float_format='%.1f')
  process_region('Barents sea')
  process_region('Norwegian sea')
  process_region('North sea')
