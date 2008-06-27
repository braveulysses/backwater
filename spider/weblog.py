#!/usr/bin/env python
# encoding: utf-8
"""
weblog.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

from source import Source
import config
import feedparser

feedparser.USER_AGENT = config.BOT_USER_AGENT

class Weblog(Source):
    def __init__(self, name, owner, url, feed_url):
        super(Weblog, self).__init__(name, owner, url)
        self.type = 'weblog'
        self.feed_url = feed_url
        self.entryType = 'post'
        self.tagline = ''

    def parse(self):
        feed_data = feedparser.parse(self.feed_url)
        print "\t" + feed_data.entries[0].title

def main():
    pass

if __name__ == '__main__':
    main()

