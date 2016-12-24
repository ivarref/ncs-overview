#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import codecs
import json
import sys
import os
import urllib

import requests
import yaml
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor

def get_m_decl(fil):
  with codecs.open(fil, 'r', encoding='utf8') as fd:
    s = fd.read()
    tree = Parser().parse(s)
    m = None
    for node in nodevisitor.visit(tree):
      if isinstance(node, ast.VarDecl) and node.identifier.value == 'm':
        m = node.initializer.to_ecma()
    return m
       
if __name__=="__main__":
  fil = sys.argv[1]
  m = get_m_decl(fil)
  js = yaml.load(m)
  self_ip = os.environ.get('self_ip', 'localhost')
  docker_ip = os.environ.get('docker_ip', 'localhost')
  for (k, v) in js.items():
    mode = k
    img = v['screenshot']
    cmd = """curl -H "Content-Type: application/json" -d '{"url":"%s:8080/bundle?mode=%s", "force": true, "width": 10, "height": 10}' http://%s:8891/ -o ./img/%s""" % (self_ip, mode, docker_ip, img)
    print(cmd.encode('utf8'))
    ret = os.system(cmd.encode('utf8'))
    print("command returned with", ret)
    if ret != 0:
      print("failure!")
      sys.exit(1)
