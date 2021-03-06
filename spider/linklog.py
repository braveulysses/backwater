#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
linklog.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2010 Spaceship No Future. All rights reserved.
"""

import logging
from urlparse import urlparse
from source import Source
from weblog import Weblog

module_logger = logging.getLogger("backwater.linklog")

class Linklog(Weblog):
    def __init__(self, name, owner, url, feed_url):
        super(Linklog, self).__init__(name, owner, url, feed_url)
        self.logger = logging.getLogger("backwater.linklog.Linklog")
        self.type = 'linklog'

    def is_delicious(self):
        domain = urlparse(self.url)[1]
        if domain == 'del.icio.us' or domain == 'delicious.com':
            return True
        else:
            return False

def main():
    pass

if __name__ == '__main__':
    main()

