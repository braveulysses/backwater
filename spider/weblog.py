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
import spider
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
        self.entry_type = 'post'
        self.tagline = ''

    def parse(self):
        """Fetches the contents of the weblog's feed and parses it.
        Each entry in the feed becomes an Entry object, and each entry attribute
        is normalized."""
        self.logger.info("Fetching feed '%s'" % self.feed_url)
        self.http_response, self.http_content = spider.fetch(self.feed_url)
        self.logger.info("Parsing feed for entries...")
        feed_data = feedparser.parse(self.feed_url)
        for entry in feed_data.entries:
            # This method will be inherited by all other feed-based 
            # sources; because we assume that the only difference between 
            # feeds of type Weblog, Linklog, and Commentlog is the presentation of 
            # their entries, instantiating the appropriate entry class here means that 
            # we don't have to write new parse() methods for Linklog and Commentlog.
            if self.type == 'linklog':
                e = Link()
            elif self.type == 'commentlog':
                e = Quote()
            else:
                e = Post()
            e.source_name = self.name
            e.source_url = self.url
            e.title = entry.get('title', '')
            self.logger.info("Entry title: '%s'" % e.title)
            e.author = entry.get('author', '')
            e.summary = entry.get('summary', '')
            e.content = entry.get('content', e.summary)
            # TODO: normalize URLs
            e.url = entry.get('link', '')
            # TODO: get via URL
            # TODO: get comments URL
            # TODO: dates
            # Done parsing this entry
            self.entries.append(e)

def main():
    #module_logger.debug("received a call to main()")
    pass

if __name__ == '__main__':
    main()

