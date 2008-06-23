#!/usr/bin/env python
# encoding: utf-8
"""
tumblelog.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

from source import Source
from weblog import Weblog

class Tumblelog(Weblog):
    def __init__(self, name, owner, url):
        super(Tumblelog, self).__init__(name, owner, url, feedUrl=None)
        self.type = 'tumblelog'

def main():
    pass

if __name__ == '__main__':
    main()

