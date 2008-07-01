#!/usr/bin/env python
# encoding: utf-8
"""
entries.py

Created by Jacob C. on 2008-06-26.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import os
import logging
import config
import spider

module_logger = logging.getLogger("backwater.entries")

class Entry(object):
    """Generic Entry object from which weblog posts, links, photos, etc. descend."""
    def __init__(self):
        super(Entry, self).__init__()
        self.source_name = ''
        self.source_url = ''
        self.title = ''
        self.author = ''
        self.summary = ''
        self.content = ''
        self.url = ''
        self.date = None
        self.published = None
        self.created = None
        self.updated = None
        self.comments = None
        self.enclosures = None
        self.tags = None
        self.via = None

    def __str__(self):
        return "'" + self.title + ",' by " + self.author

class Post(Entry):
    def __init__(self):
        super(Post, self).__init__()

class Link(Entry):
    def __init__(self):
        super(Link, self).__init__()
        
class Quote(Entry):
    def __init__(self):
        super(Quote, self).__init__()

class Conversation(Entry):
    def __init__(self):
        super(Conversation, self).__init__()

class Song(Entry):
    def __init__(self):
        super(Song, self).__init__()

class Video(Entry):
    def __init__(self):
        super(Video, self).__init__()

class Photo(Entry):
    def __init__(self):
        super(Photo, self).__init__()
        self.logger = logging.getLogger("backwater.entries.Photo")
        self.id = ''
        self.secret = ''
        self.server = ''
        # self.photo_url is a URL for the photo itself
        # self.url is a URL for the photo's web page
        self.photo_url = ''

    def get_cached_original_fn(self):
        return "%s%s_%s_orig.jpg" % (config.IMAGE_CACHE_DIR, self.id, self.secret)

    def get_cached_thumbnail_fn(self):
        return "%s%s_%s_thumb.jpg" % (config.IMAGE_CACHE_DIR, self.id, self.secret)

    def cache(self):
        try:
            self.logger.info("Fetching and caching photo '%s'" % self.title)
            content_types = [
                'image/jpeg',
                'image/gif'
            ]
            resp, content = spider.fetch(self.photo_url, valid_content_types=content_types)
            self.logger.debug('HTTP Status: %s' % str(resp.status))
            if resp.status == 200:
                self.logger.debug('Saving photo to cache')
                f = open(self.get_cached_original_fn(), 'w')
                f.write(content)
                f.close()
        except:
            self.logger.exception("Problem caching photo!")

def main():
    pass

if __name__ == '__main__':
    main()

