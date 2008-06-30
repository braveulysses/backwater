#!/usr/bin/env python
# encoding: utf-8
"""
commentlog.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import logging
from source import Source
from weblog import Weblog
from entries import Quote

module_logger = logging.getLogger("backwater.commentlog")

class Commentlog(Weblog):
    def __init__(self, name, owner, url, feed_url):
        super(Commentlog, self).__init__(name, owner, url, feed_url)
        self.logger = logging.getLogger("backwater.commentlog.Commentlog")
        self.type = 'commentlog'
        self.entry_type = 'quote'

def main():
    pass

if __name__ == '__main__':
    main()

