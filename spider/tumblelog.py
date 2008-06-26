#!/usr/bin/env python
# encoding: utf-8
"""
tumblelog.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

from source import Source
from weblog import Weblog
import tumblr

class Tumblelog(Weblog):
    def __init__(self, name, owner, url):
        super(Tumblelog, self).__init__(name, owner, url, feed_url=None)
        self.type = 'tumblelog'
        self.entry_type = None
        self.api_url = url + 'api/read'

    def parse(self):
        t = tumblr.parse(self.api_url)
        print t.posts[0].content

def main():
    pass

if __name__ == '__main__':
    main()

