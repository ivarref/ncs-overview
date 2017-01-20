#!/usr/bin/env python3

import pandas as pd

if __name__=="__main__":
  frame = pd.read_csv('./data/raw_discovery_resources.csv')
  resource_types = sorted(frame.dscReservesRC.unique())

  for resource_type in resource_types:
    f = frame[frame['dscReservesRC'] == resource_type]
    oil = f.dscRecoverableOil.sum()
    gas = f.dscRecoverableGas.sum()
    oe = f.dscRecoverableOe.sum()
    def fmt(x):
      return "%.1f" % ((x*6.29) / 1000.0)
    print(resource_type, fmt(oil), fmt(gas), fmt(oe))
  
  print("Sum", fmt(frame.dscRecoverableOil.sum()), fmt(frame.dscRecoverableGas.sum()), fmt(frame.dscRecoverableOe.sum()))
