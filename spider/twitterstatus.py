#!/usr/bin/env python
# encoding: utf-8
"""
twitterstatus.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

from source import Source

class TwitterStatus(Source):
    def __init__(self, name, owner, url):
        super(TwitterStatus, self).__init__(name, owner, url)
        self.type = 'twitterstatus'
        self.entryType = 'quote'

def main():
    pass

if __name__ == '__main__':
    main()

