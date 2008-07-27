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
from feedparser import _parse_date as parse_date
from BeautifulSoup import BeautifulSoup
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
    def __init__(self, name, owner, url, excluded_types=None):
        super(Tumblelog, self).__init__(name, owner, url, feed_url=None)
        self.logger = logging.getLogger("backwater.tumblelog.Tumblelog")
        self.type = 'tumblelog'
        self.entry_type = None
        self.api_url = url + 'api/read'
        self.excluded_types = excluded_types

    def parse(self):
        """Fetches Tumblr API data and parses it."""
        self.logger.info("Fetching API data at '%s'" % self.api_url)
        self.http_response, self.http_content = spider.fetch(self.api_url)
        self.logger.info("Parsing API data for entries...")
        t = tumblr.parse(self.api_url)
        for post in t.posts:
            try:
                if post.type == 'regular':
                    self.logger.info("Tumblr post type: regular")
                    e = Post()
                    e.title = post.title
                    e.summary = post.content
                    e.content = post.content
                elif post.type == 'link':
                    if 'link' in self.excluded_types:
                        self.logger.debug("Skipping Tumblr link")
                        continue
                    else:
                        self.logger.info("Tumblr post type: link")
                        e = Link()
                        e.title = post.title
                        e.summary = post.content
                        e.content = post.content
                        e.url = post.related
                        e.comments = post.url
                elif post.type == 'quote':
                    self.logger.info("Tumblr post type: quote")
                    e = Quote()
                    e.summary = post.content
                    # Chop the smart quotes that Tumblr automatically 
                    # adds to to a quote                
                    e.summary = e.summary.lstrip("&#8220;").rstrip("&#8221;")
                    e.content = e.summary
                    # Get the quote's citation, and, if possible its source
                    e.citation = post.source
                    try:
                        soup = BeautifulSoup(e.citation)
                        e.citation_url = soup.find('a').get('href')
                        e.via = e.citation_url
                    except AttributeError:
                        e.citation_url = None
                elif post.type == 'photo':
                    self.logger.info("Tumblr post type: photo")
                    e = Photo()
                    e.photo_type = 'tumblr'
                    e.title = ''
                    e.summary = post.caption
                    e.content = e.summary
                    # post.urls is a dictionary of photo URLs keyed by size.
                    # Let's get the big one.
                    e.photo_url = post.urls['500']
                    e.cached_url = config.IMAGES_URL + '/' + e._get_cached_original_shortname()
                    self.logger.debug("Tumblr photo URL: '%s'" % e.photo_url)
                    e.cache()
                    e.set_dimensions()
                # Conversation, Video, and Audio post types aren't 
                # going to be implemented for a while
                elif post.type == 'conversation':
                    self.logger.info("Tumblr post type: conversation")
                    continue
                    #e = Conversation()
                elif post.type == 'video':
                    self.logger.info("Tumblr post type: video")
                    continue
                    #e = Video()
                elif post.type == 'audio':
                    self.logger.info("Tumblr post type: audio")
                    continue
                    #e = Audio()
                e.source.name = self.name
                e.source.url = self.url
                if e.url == '':
                    e.url = post.url
                e.author = self.owner
                e.date = post.date
                e.date_parsed = parse_date(post.date)
                self.logger.debug("Tumblr post date: %s" % e.date_as_string(e.date_parsed))
                self.logger.info("Entry title: '%s'" % e.title)
                self.logger.debug("Entry URL: '%s'" % e.url)
                self.entries.append(e)
            except AttributeError:
                # FIXME: Why is this exception handler here???
                pass

def main():
    pass

if __name__ == '__main__':
    main()

