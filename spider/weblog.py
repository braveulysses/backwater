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
        Each entry in the feed becomes an Entry object, and each entry 
        attribute is normalized."""
        self.logger.info("Fetching feed '%s'" % self.feed_url)
        self.http_response, self.http_content = spider.fetch(self.feed_url)
        self.logger.info("Parsing feed for entries...")
        feed_data = feedparser.parse(self.feed_url)
        self.id = feed_data.feed.get('id', '')
        self.name = feed_data.feed.get('title', self.name)
        self.generator = feed_data.feed.get('generator', None)
        self.url = feed_data.feed.get('url', self.url)
        self.updated = feed_data.feed.get('updated', None)
        self.updated_parsed = feed_data.feed.get('updated_parsed', None)
        self.rights = feed_data.feed.get('rights', None)
        for entry in feed_data.entries:
            # This method will be inherited by all other feed-based 
            # sources; because we assume that the only difference between 
            # feeds of type Weblog, Linklog, and Commentlog is the 
            # presentation of their entries, instantiating the appropriate 
            # entry class here means that we don't have to write new 
            # parse() methods for Linklog and Commentlog.
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
            # TODO: Need to get 'content["value"]', not just 'content'
            e.content = entry.get('content', e.summary)
            # TODO: Handle 'rel', 'alternate', and 'via' links correctly
            # Atom weblog feeds should used 'rel="related"' for 
            # the linked page, so need to make sure we get that link 
            # and not the 'alternate' or 'via' link.
            # TODO: Normalize URLs
            e.url = entry.get('link', '')
            # TODO: Get via URL
            # TODO: Get comments URL
            e.date = entry.get('date')
            e.date_parsed = entry.get('date_parsed')
            self.logger.debug("Entry date: %s" % e.date_as_string(e.date_parsed))
            e.published = entry.get('published', e.date)
            e.published_parsed = entry.get('published_parsed', e.date_parsed)
            e.updated = entry.get('updated', e.date)
            e.updated_parsed = entry.get('updated_parsed', e.date_parsed)
            e.created = entry.get('created', e.date)
            e.created_parsed = entry.get('created_parsed', e.date_parsed)
            # Done parsing this entry
            self.entries.append(e)

def main():
    #module_logger.debug("received a call to main()")
    pass

if __name__ == '__main__':
    main()

