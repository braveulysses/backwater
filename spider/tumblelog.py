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
                if post.type == 'link':
                    self.logger.info("Tumblr post type: link")
                    e = Link()
                    e.title = post.title
                    e.summary = post.content
                    e.content = post.content
                    e.related = post.related
                elif post.type == 'quote':
                    self.logger.info("Tumblr post type: quote")
                    e = Quote()
                    e.summary = post.content
                    e.content = post.content
                    e.citation = post.source
                elif post.type == 'photo':
                    self.logger.info("Tumblr post type: photo")
                    e = Photo()
                    e.summary = post.caption
                    # TODO: fetch, resize, and cache photo
                # Conversation, Video, and Audio post types aren't 
                # going to be implemented for a while
                # elif post.type = 'conversation':
                #     self.logger.info("Tumblr post type: conversation")
                #     e = Conversation()
                # elif post.type = 'video':
                #     self.logger.info("Tumblr post type: video")
                #     e = Video()
                # elif post.type = 'audio':
                #     self.logger.info("Tumblr post type: audio")
                #     e = Audio()
                else:
                    self.logger.info("Tumblr post type: regular")
                    e = Post()
                    e.title = post.title
                    e.summary = post.content
                    e.content = post.content
                e.source_name = self.name
                e.source_url = self.url
                e.url = post.url
                e.date = post.date
                self.logger.info("Entry title: '%s'" % e.title)
                self.logger.debug("Entry content: '%s'" % e.content)
                self.entries.append(e)
            except AttributeError:
                pass

def main():
    pass

if __name__ == '__main__':
    main()

