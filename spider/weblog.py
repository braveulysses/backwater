#!/usr/bin/env python
# encoding: utf-8
"""
weblog.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

from source import Source

class Weblog(Source):
    def __init__(self, name, owner, url, feedUrl):
        super(Weblog, self).__init__(name, owner, url)
        self.type = 'weblog'
        self.feedUrl = feedUrl

def main():
    pass

if __name__ == '__main__':
    main()

