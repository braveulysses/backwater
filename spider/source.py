#!/usr/bin/env python
# encoding: utf-8
"""
source.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

class Source(object):
    def __init__(self, name, owner, url):
        super(Source, self).__init__()
        self.type = 'source'
        self.name = name
        self.owner = owner
        self.url = url
        self.entries = []
        self.httpResponse = None

    def parse(): pass

def main():
	pass

if __name__ == '__main__':
	main()

