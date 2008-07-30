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
from entries import AtomSource
from entries import Entry
from entries import Post
from entries import Link
from entries import Quote
from publish.sanitizer import sanitize

feedparser.USER_AGENT = config.BOT_USER_AGENT

module_logger = logging.getLogger("backwater.weblog")

class Weblog(Source):
    def __init__(self, name, owner, url, feed_url):
        super(Weblog, self).__init__(name, owner, url)
        self.logger = logging.getLogger("backwater.weblog.Weblog")
        #self.logger.debug("Created an instance of Weblog: '%s'" % self.name)
        self.type = 'weblog'
        self.feed_url = feed_url
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
        self.url = feed_data.feed.get('link', self.url)
        self.logger.debug("Weblog URL: '%s'" % self.url)
        self.tagline = feed_data.feed.get('tagline', '')
        self.updated = feed_data.feed.get('updated', None)
        self.updated_parsed = feed_data.feed.get('updated_parsed', None)
        self.rights = feed_data.feed.get('rights', None)
        if feed_data.version.find('atom', 0, 4) == 0:
            self.atom = True
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
            e.source.name = self.name
            e.source.url = self.url
            e.atom = self.atom
            e.title = entry.get('title', '')
            self.logger.info("Entry title: '%s'" % e.title)
            e.author = entry.get('author', self.owner)
            try:
                e.author_url = entry.author_detail['href']
            except (AttributeError, KeyError):
                e.author_url = None
            e.summary = entry.get('summary', '')
            # Need to get 'content[x]["value"]', not just 'content', 
            # and we prefer something marked "text/html"
            try:
                html_types = [
                    'text/html',
                    'application/xhtml+xml',
                    'application/xml',
                    'text/xml',
                    'text/plain'
                ]
                for content in entry['content']:
                    if content['type'] in html_types:
                        e.content = content['value']
                        continue
            except (KeyError, IndexError, AttributeError):
                e.content = e.summary
            # Atom weblog feeds should used 'rel="related"' for 
            # the linked page, so need to make sure we get that link 
            # and not the 'alternate' or 'via' link.
            e.url = entry.get('link', None)
            for link in entry.links:
                if link['rel'] == 'via':
                    e.via = link['href']
                    break
                else:
                    e.via = None
            for link in entry.links:
                if link['rel'] == 'related':
                    e.url = link['href']
                    break
                else:
                    e.url = entry.link
            e.comments = entry.get('comments', None)
            # 'alternate' represents the linklog entry itself, 
            # which is often a comments page
            if self.type == 'linklog':
                e.comments = e.get_delicious_url()
            if e.comments is None:
                for link in entry.links:
                    if link['rel'] == 'alternate':
                        e.comments = link['href']
            # Now, get tags/categories
            try:
                if len(entry.tags) > 0:
                    if e.type == 'link' and self.is_delicious():
                        # del.icio.us tags need to be coaxed out...
                        # See: http://code.google.com/p/feedparser/issues/detail?id=34
                        e.tags = entry.tags[0].term.split()
                    else:
                        for tag in entry.tags:
                            e.tags.append(tag.term)
            except AttributeError:
                # No tags! Forget it.
                pass
            # Nix the comments property if it's the same link as the permalink
            if e.url == e.comments:
                e.comments = None
            # Put together the Atom <source> info, if applicable
            if e.atom:
                e.atom_source = AtomSource()
                try:
                    e.atom_source.id = self.id
                    e.atom_source.title = sanitize(self.name)
                    e.atom_source.url = self.url
                    e.atom_source.updated = self.updated
                except AttributeError:
                    self.logger.exception("Trouble getting Atom source for '%s'!" % self.name)
                    e.atom_source = None
            else:
                e.atom_source = None
            # DATES!
            e.date = entry.get('date')
            e.date_parsed = entry.get('date_parsed')
            self.logger.debug("Entry date: %s" % e.date_as_string(e.date_parsed))
            e.published = entry.get('published', e.date)
            e.published_parsed = entry.get('published_parsed', e.date_parsed)
            e.updated = entry.get('updated', e.date)
            e.updated_parsed = entry.get('updated_parsed', e.date_parsed)
            e.created = entry.get('created', e.date)
            e.created_parsed = entry.get('created_parsed', e.date_parsed)
            # Build GUID
            if e.atom:
                e.id = entry.get('id')
            else:
                e.id = e.get_tag_uri(e.date_parsed, e.url)
            # Done parsing this entry
            self.entries.append(e)

def main():
    #module_logger.debug("received a call to main()")
    pass

if __name__ == '__main__':
    main()

