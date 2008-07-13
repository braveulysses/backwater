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

module_logger = logging.getLogger("backwater.linklog")

class Linklog(Weblog):
    def __init__(self, name, owner, url, feed_url):
        super(Linklog, self).__init__(name, owner, url, feed_url)
        self.logger = logging.getLogger("backwater.linklog.Linklog")
        self.type = 'linklog'
        self.entry_type = 'link'

def main():
    pass

if __name__ == '__main__':
    main()

