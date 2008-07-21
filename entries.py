#!/usr/bin/env python
# encoding: utf-8
"""
entries.py

Created by Jacob C. on 2008-06-26.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import os
import time 
import logging
import config
import spider
from urlparse import urlparse
from feedparser import _parse_date as parse_date

module_logger = logging.getLogger("backwater.entries")

class NotAnEntryError(Exception): pass

class Entry(object):
    """Generic Entry object from which weblog posts, links, photos, 
    etc. descend.
    """
    def __init__(self):
        super(Entry, self).__init__()
        self.type = None
        self.source_name = ''
        self.source_url = ''
        # Id needs to be a unique and permanent identifier
        self.id = None
        self.title = ''
        self.author = ''
        self.summary = ''
        self.content = ''
        # Url = permalink
        self.url = ''
        # Related is generally used as a pointer to the source link, 
        # especially in linklogs
        self.related = None
        # Via is generally used for a source credit
        self.via = None
        self.comments = None
        # Date is a synonym for Published
        self.date = None
        self.date_parsed = None
        self.published = None
        self.published_parsed = None
        self.created = None
        self.created_parsed = None
        self.updated = None
        self.updated_parsed = None
        self.comments = None
        self.enclosures = None
        self.tags = None
        self.categories = None
        # Rights is generally used for a copyright statement
        self.rights = None
        # TODO: support Atom source element:
        # http://www.atomenabled.org/developers/syndication/atom-format-spec.php#element.source
        # This is not quite the same as a via reference.

    def __str__(self):
        return "'" + self.title + ",' by " + self.author
    
    def __cmp__(self, other):
        if isinstance(other, Entry):
            return cmp(self.date_parsed, other.date_parsed)
        else:
            raise NotAnEntryError
        
    def date_as_string(self, t):
        """Given a datetime tuple, returns a string representation.
        Uses the format Month Day, YYYY HH:MM AM/PM"""
        return time.strftime("%B %d, %Y %H:%M %p", t)
        
    def normalize(self):
        """Checks that all attribute values are in order so that the entry 
        can be used for output, particularly in an Atom feed."""
        if self.content == '':
            self.content == self.summary
        if self.published is None:
            self.published == self.date
        if self.published_parsed is None:
            self.published_parsed = parse_date(self.published)
        if self.created is None:
            self.created == self.date
        if self.created_parsed is None:
            self.created_parsed = parse_date(self.created)
        if self.updated is None:
            self.updated == self.date
        if self.updated_parsed is None:
            self.updated_parsed = parse_date(self.updated)

class Post(Entry):
    def __init__(self):
        super(Post, self).__init__()
        self.type = 'post'

class Link(Entry):
    def __init__(self):
        super(Link, self).__init__()
        self.type = 'link'
        
class Quote(Entry):
    def __init__(self):
        super(Quote, self).__init__()
        self.type = 'quote'
        # This is awkward, but since 'source' is already taken...
        # citation = source of the quote
        self.citation = ''

class Conversation(Entry):
    def __init__(self):
        super(Conversation, self).__init__()
        self.type = 'conversation'

class Song(Entry):
    def __init__(self):
        super(Song, self).__init__()
        self.type = 'song'

class Video(Entry):
    def __init__(self):
        super(Video, self).__init__()
        self.type = 'video'

class Photo(Entry):
    def __init__(self):
        super(Photo, self).__init__()
        self.type = 'photo'
        self.logger = logging.getLogger("backwater.entries.Photo")
        self.id = ''
        self.farm_id = ''
        self.secret = ''
        self.server = ''
        # self.photo_url is a URL for the photo itself
        # self.url is a URL for the photo's web page
        self.photo_url = ''
        # The self.cache() method needs to know whether the photo originated 
        # from Tumblr or Flickr, so stick it in self.photo_type
        self.photo_type = ''

    def _get_flickr_photo_url(self, farm_id, server, photo_id, secret):
        return 'http://farm%s.static.flickr.com/%s/%s_%s.jpg' % (
            farm_id, 
            server, 
            photo_id, 
            secret
        )

    def _get_flickr_url(self, flickr_id, photo_id):
        return 'http://www.flickr.com/photos/%s/%s/' % (flickr_id, photo_id)

    def _get_cached_original_fn(self):
        if self.photo_type == 'flickr':
            return "%s/flickr_orig_%s_%s.jpg" % (config.IMAGE_CACHE_DIR, self.id, self.secret)
        elif self.photo_type == 'tumblr':
            # We don't necessarily know that the photo will be a JPEG.  To 
            # be safe, let's just take the path component of the URL and 
            # use that (after removing any slashes).
            tumblr_photo_path = urlparse(self.photo_url)[2].replace('/', '')
            return "%s/tumblr_orig_%s" % (config.IMAGE_CACHE_DIR, tumblr_photo_path)
        else:
            # ???
            raise Exception

    def _get_cached_thumbnail_fn(self):
        if self.photo_type == 'flickr':
            return "%s/flickr_thumb_%s_%s.jpg" % (config.IMAGE_CACHE_DIR, self.id, self.secret)
        elif self.photo_type == 'tumblr':
            # See get_cached_original_fn()
            tumblr_photo_path = urlparse(self.photo_url)[2].replace('/', '')
            return "%s/tumblr_thumb_%s" % (config.IMAGE_CACHE_DIR, tumblr_photo_path)
        else:
            # ???
            raise Exception

    def resize(self):
        # TODO: resize photos
        pass

    def cache(self):
        """Fetches photo via HTTP and caches both the original and a 
        thumbnail.
        """
        try:
            self.logger.info("Fetching and caching photo '%s'" % self.title)
            content_types = [
                'image/jpeg',
                'image/gif',
                'image/png'
            ]
            resp, content = spider.fetch(self.photo_url, valid_content_types=content_types)
            self.logger.debug('HTTP Status: %s' % str(resp.status))
            if resp.status == 200:
                self.logger.debug('Saving photo to cache')
                f = open(self._get_cached_original_fn(), 'w')
                f.write(content)
                f.close()
            # TODO: create thumbnail
        except:
            self.logger.exception("Problem caching photo!")

def main():
    pass

if __name__ == '__main__':
    main()

