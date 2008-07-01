#!/usr/bin/env python
# encoding: utf-8
"""
tumblelog.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import logging
import config
import spider
import tumblr
from source import Source
from weblog import Weblog
from entries import Entry
from entries import Post
from entries import Link
from entries import Quote
from entries import Conversation
from entries import Song
from entries import Video
from entries import Photo

tumblr.USER_AGENT = config.BOT_USER_AGENT

module_logger = logging.getLogger("backwater.tumblelog")

class Tumblelog(Weblog):
    def __init__(self, name, owner, url):
        super(Tumblelog, self).__init__(name, owner, url, feed_url=None)
        self.logger = logging.getLogger("backwater.tumblelog.Tumblelog")
        self.logger.debug("Created an instance of Tumblelog: '%s'" % self.name)
        self.type = 'tumblelog'
        self.entry_type = None
        self.api_url = url + 'api/read'

    def parse(self):
        """Fetches Tumblr API data and parses it."""
        self.logger.info("Fetching API data at '%s'" % self.api_url)
        self.http_response, self.http_content = spider.fetch(self.api_url)
        self.logger.info("Parsing API data for entries...")
        t = tumblr.parse(self.api_url)
        for post in t.posts:
            try:
                self.logger.info("Entry title: '%s'" % post.title)
            except AttributeError:
                pass

def main():
    pass

if __name__ == '__main__':
    main()

