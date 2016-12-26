#!/usr/bin/env python3

import pandas as pd

if __name__=="__main__":
  frame = pd.read_csv('data/raw_wellbore.csv')
  print("number of all wellbores:", len(frame))
  frame = frame[frame["wlbPurpose"] == "WILDCAT"]
  print("number of WILDCAT wellbores:", len(frame))
  
  areas = frame['wlbMainArea'].unique()
  reserves = pd.read_csv('data/region/reserves_gboe_by_region.csv')
  print(80*'*')

  per_well_reserves = []
  for area in areas:
    f = frame[frame['wlbMainArea'] == area]
    r = reserves[reserves['name'] == area]['origRecoverableOE'].values[0] * 1000.0
    per_well_reserves.append((area, r/len(f)))
  mx = max([x[1] for x in per_well_reserves])
  for (area, per_well) in per_well_reserves:
    print(area, per_well/mx * 100.0)
  print(per_well_reserves)
  print(80*'*')
