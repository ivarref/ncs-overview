#!/usr/bin/env python3

import glob
import screens_from_page

if __name__=="__main__":
  for fil in glob.glob("vis/*.js"):
    m = screens_from_page.get_m_decl(fil)
    if m != None:
      print(fil),
