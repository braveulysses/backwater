#!/usr/bin/env python
# encoding: utf-8
"""
weblog.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import config
import feedparser
import logging
from source import Source
from entries import Entry
from entries import Post
from entries import Link
from entries import Quote

feedparser.USER_AGENT = config.BOT_USER_AGENT

module_logger = logging.getLogger("backwater.weblog")

class Weblog(Source):
    def __init__(self, name, owner, url, feed_url):
        super(Weblog, self).__init__(name, owner, url)
        self.logger = logging.getLogger("backwater.weblog.Weblog")
        #self.logger.debug("Created an instance of Weblog: '%s'" % self.name)
        self.type = 'weblog'
        self.feed_url = feed_url
        self.entryType = 'post'
        self.tagline = ''

    def parse(self):
        self.logger.info("Fetching feed '%s'" % self.feed_url)
        self.fetch(self.feed_url)
        self.logger.info("Parsing feed for entries...")
        feed_data = feedparser.parse(self.feed_url)
        for entry in feed_data.entries:
            # This method will be inherited by all other feed-based 
            # sources, so instantiate the appropriate entry class
            if self.type == 'linklog':
                e = Link()
            elif self.type == 'commentlog':
                e = Quote()
            else:
                e = Post()
            # Title
            e.title = entry.get('title', '')
            self.logger.info("Entry title: '%s'" % e.title)
            # Author
            e.author = entry.get('author', '')
            # Summary
            e.summary = entry.get('summary', '')
            # Content
            e.content = entry.get('content', e.summary)
            # URL
            e.url = entry.get('link', '')
            # Done parsing this entry
            self.entries.append(e)

def main():
    #module_logger.debug("received a call to main()")
    pass

if __name__ == '__main__':
    main()

