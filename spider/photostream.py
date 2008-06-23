#!/usr/bin/env python
# encoding: utf-8
"""
photostream.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

from source import Source

class Photostream(Source):
    def __init__(self, name, owner, url, flickrId):
        super(Photostream, self).__init__(name, owner, url)
        self.type = 'photostream'
        self.flickrId = flickrId

def main():
    pass

if __name__ == '__main__':
    main()

