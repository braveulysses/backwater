#!/usr/bin/env python
# encoding: utf-8
"""
source.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import logging
import config

module_logger = logging.getLogger("backwater.source")

def source_string(name, type, owner, url):
    return """%s
  Type: %s
  Owner: %s
  URL: %s""" % (name, type, owner, url)

class Source(object):
    def __init__(self, name, owner, url):
        super(Source, self).__init__()
        self.logger = logging.getLogger("backwater.source.Source")
        self.type = 'source'
        self.entry_type = None
        self.name = name
        self.owner = owner
        self.url = url
        self.entries = []
        self.http_content = None
        self.http_response = None

    def __str__(self):
        return source_string(self.name, self.type, self.owner, self.url)

    def parse(self): pass

def main():
	pass

if __name__ == '__main__':
	main()

