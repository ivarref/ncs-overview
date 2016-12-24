#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import sys

import yaml

if __name__=="__main__":
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
    def dict_representer(dumper, data):
        return dumper.represent_dict(data.iteritems())
    def dict_constructor(loader, node):
        return collections.OrderedDict(loader.construct_pairs(node))
    yaml.add_representer(collections.OrderedDict, dict_representer)
    yaml.add_constructor(_mapping_tag, dict_constructor)

    with open('./extra_data/discovery_overview_extra.yml') as fd:
        d = yaml.load(fd)
        print(",".join(d.keys()))
        print(",".join([str(x) for x in d.values()]))
