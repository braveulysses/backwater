#!/usr/bin/env python
# encoding: utf-8
"""
twitterstatus.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import logging
import config
from source import Source
from entries import Quote

module_logger = logging.getLogger("backwater.twitterstatus")

class TwitterStatus(Source):
    def __init__(self, name, owner, url):
        super(TwitterStatus, self).__init__(name, owner, url)
        self.logger = logging.getLogger("backwater.twitterstatus.TwitterStatus")
        self.type = 'twitterstatus'
        self.entry_type = 'quote'

def main():
    pass

if __name__ == '__main__':
    main()

