#!/usr/bin/env python
# encoding: utf-8
"""
source.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

#from text import u
import config

class Source(object):
    def __init__(self, name, owner, url):
        super(Source, self).__init__()
        self.type = 'source'
        self.entry_type = None
        self.name = name
        self.owner = owner
        self.url = url
        self.entries = []
        self.http_content = None
        self.http_response = None

    def __str__(self):
        return "%s: %s" % (self.type, self.name)

    def fetch(self): pass

    def parse(self): pass

def main():
	pass

if __name__ == '__main__':
	main()
