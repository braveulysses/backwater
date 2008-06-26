#!/usr/bin/env python
# encoding: utf-8
"""
commentlog.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

from source import Source
from weblog import Weblog

class Commentlog(Weblog):
    def __init__(self, name, owner, url, feed_url):
        super(Commentlog, self).__init__(name, owner, url, feed_url)
        self.type = 'commentlog'
        self.entry_type = 'quote'

def main():
    pass

if __name__ == '__main__':
    main()

