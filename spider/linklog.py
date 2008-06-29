#!/usr/bin/env python
# encoding: utf-8
"""
linklog.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import logging
from source import Source
from weblog import Weblog

class Linklog(Weblog):
    def __init__(self, name, owner, url, feedUrl):
        super(Linklog, self).__init__(name, owner, url, feedUrl)
        self.logger = logging.getLogger("backwater.linklog.Linklog")
        self.type = 'linklog'
        self.entryType = 'link'

def main():
    pass

if __name__ == '__main__':
    main()

