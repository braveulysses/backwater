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
import urllib
import md5
import Image
import config
import spider
import publish.shorten
import publish.sanitizer
from urlparse import urlparse
from feedparser import _parse_date as parse_date

module_logger = logging.getLogger("backwater.entries")

class NotAnEntryError(Exception): pass
class NonexistentImageError(Exception): pass

class EntrySource(object):
    """Stores attributes pertaining to an entry's source (i.e., weblog, tumblelog, etc.).
    We don't store a reference to the Source object to allow for garbage collection.
    """
    def __init__(self):
        super(EntrySource, self).__init__()
        self.name = ''
        self.url = ''

class AtomSource(object):
    """Representation of an Atom <source> element.
    
    See <http://www.atomenabled.org/developers/syndication/atom-format-spec.php#element.source>
    """
    def __init__(self):
        super(AtomSource, self).__init__()
        self.id = None
        self.title = None
        self.url = None
        self.updated = None

class Entry(object):
    """Generic Entry object from which weblog posts, links, photos, 
    etc. descend.
    """
    def __init__(self):
        super(Entry, self).__init__()
        self.type = None
        self.source = EntrySource()
        self.atom = False
        self.id = None
        self.title = ''
        self.author = ''
        self.author_url = None
        self.summary = ''
        self.content = ''
        self.content_abridged = ''
        # Url = permalink
        self.url = ''
        # Related is generally used as a pointer to the source link, 
        # especially in linklogs
        self.related = None
        # Via is generally used for a source credit
        self.via = None
        self.atom_source = None
        self.comments = None
        # TODO: Detect enclosures
        self.enclosures = None
        # TODO: Get tags/categories
        self.tags = None
        self.categories = None
        # Rights is generally used for a copyright statement
        self.rights = None
        # Date is a synonym for Published
        self.date = None
        self.date_parsed = None
        self.published = None
        self.published_parsed = None
        self.created = None
        self.created_parsed = None
        self.updated = None
        self.updated_parsed = None
        # Atom formatted dates
        self.date_atom = None
        self.published_atom = None
        self.created_atom = None
        self.updated_atom = None
        # Friendly-formatted dates
        self.date_formatted = None
        self.published_formatted = None
        self.created_formatted = None
        self.updated_formatted = None

    def __str__(self):
        return "'" + self.title + ",' by " + self.author
    
    def __cmp__(self, other):
        if isinstance(other, Entry):
            return cmp(self.published_parsed, other.published_parsed)
        else:
            raise NotAnEntryError

    def get_tag_uri(self, date, url):
        """Constructs a tag URI for use as a feed GUID.
        Takes a date tuple and a URL as arguments."""
        tagURI = []
        url = url.replace('#', '/')
        parsed_url = urlparse(url)
        date = time.strftime("%Y-%m-%d", date)
        tagURI.append('tag:chompy.net,')
        tagURI.append(date)
        tagURI.append(':')
        tagURI.append(urllib.quote_plus(parsed_url[1]))
        tagURI.append(':')
        tagURI.append(urllib.quote_plus(parsed_url[2]))
        if parsed_url[3] != '':
            tagURI.append(urllib.quote_plus(parsed_url[3]))
        if parsed_url[4] != '':
            tagURI.append('?')
            tagURI.append(urllib.quote_plus(parsed_url[4]))
        if parsed_url[5] != '':
            tagURI.append('#')
            tagURI.append(urllib.quote_plus(parsed_url[5]))
        #tagURI.append(urlnorm.normalize(parsed_url[2]))
        return ''.join(tagURI)

    def date_as_string(self, t):
        """Given a datetime tuple, returns a string representation.
        Uses the format: Month Day, YYYY HH:MM AM/PM
        
        Pretty much used when debugging."""
        return time.strftime("%B %d, %Y %H:%M %p", t)
        
    def normalize(self):
        """Checks that all attribute values are in order so that the entry 
        can be used for output, particularly in an Atom feed."""
        if self.title is None:
            self.title = ''
        if self.summary is None:
            self.summary = ''
        if self.content == '' or self.content is None:
            self.content = self.summary
        if self.published is None:
            self.published = self.date
        if self.published_parsed is None:
            self.published_parsed = parse_date(self.published)
        if self.created is None:
            self.created = self.date
        if self.created_parsed is None:
            self.created_parsed = parse_date(self.created)
        if self.updated is None:
            self.updated = self.date
        if self.updated_parsed is None:
            self.updated_parsed = parse_date(self.updated)
        self.date_atom = time.strftime(config.ATOM_TIME_FORMAT, self.date_parsed)
        self.published_atom = time.strftime(config.ATOM_TIME_FORMAT, self.published_parsed)
        self.created_atom = time.strftime(config.ATOM_TIME_FORMAT, self.created_parsed)
        self.updated_atom = time.strftime(config.ATOM_TIME_FORMAT, self.updated_parsed)            
        self.date_formatted = time.strftime(config.HTML_TIME_FORMAT, self.date_parsed)
        self.published_formatted = time.strftime(config.HTML_TIME_FORMAT, self.published_parsed)
        self.created_formatted = time.strftime(config.HTML_TIME_FORMAT, self.created_parsed)
        self.updated_formatted = time.strftime(config.HTML_TIME_FORMAT, self.updated_parsed)
        # Build GUID
        if self.id is None:
            self.id = self.get_tag_uri(self.date_parsed, self.url)
        # Truncate content for main page
        if publish.shorten.wc(self.content) > config.WORD_LIMIT:
            self.content_abridged = publish.shorten.shorten(self.content, config.WORD_LIMIT)
        else:
            self.content_abridged = self.content
        # Sanitize content
        self.title = publish.sanitizer.sanitize(self.title)
        self.summary = publish.sanitizer.strip(self.summary)
        #self.summary = publish.sanitizer.sanitize(self.summary)
        # If the entry is a photo, allow <img> tag
        if self.type == 'photo':
            self.content = publish.sanitizer.sanitize(self.content, additional_tags=[ 'img' ])
        else:
            self.content = publish.sanitizer.sanitize(self.content)
        self.content_abridged = publish.sanitizer.sanitize(self.content_abridged)
        # Escape content
        #self.title = publish.sanitizer.escape(self.title)
        #self.summary = publish.sanitizer.escape(self.summary)
        #self.content = publish.sanitizer.escape_amps_only(self.content)
        #self.content_abridged = publish.sanitizer.escape_amps_only(self.content_abridged)

class Post(Entry):
    def __init__(self):
        super(Post, self).__init__()
        self.type = 'post'

class Link(Entry):
    def __init__(self):
        super(Link, self).__init__()
        self.type = 'link'

    def get_delicious_url(self):
        """Gets the del.icio.us permalink for the current entry."""
        m = md5.new()
        m.update(self.url)
        return 'http://del.icio.us/url/' + m.hexdigest()
        
class Quote(Entry):
    def __init__(self):
        super(Quote, self).__init__()
        self.type = 'quote'
        # This is awkward, but since 'source' is already taken...
        # citation = source of the quote
        self.citation = ''
        self.citation_url = None

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
        self.photo_id = ''
        self.farm_id = ''
        self.secret = ''
        self.server = ''
        # self.photo_url is a URL for the photo itself
        # self.cached_url is a URL for a copy of the photo itself
        # self.url is a URL for the photo's web page
        self.photo_url = ''
        self.cached_url = ''
        # The self.cache() method needs to know whether the photo originated 
        # from Tumblr or Flickr, so stick it in self.photo_type
        self.photo_type = ''
        self.height = 0
        self.width = 0

    def _get_flickr_photo_url(self, farm_id, server, photo_id, secret):
        return 'http://farm%s.static.flickr.com/%s/%s_%s.jpg' % (
            farm_id, 
            server, 
            photo_id, 
            secret
        )

    def _get_flickr_url(self, flickr_id, photo_id):
        return 'http://www.flickr.com/photos/%s/%s/' % (flickr_id, photo_id)

    def _get_cached_original_shortname(self):
        """This returns the cached original photo's filename, without the leading path.
        Useful when constructing a URL."""
        if self.photo_type == 'flickr':
            return "flickr_orig_%s_%s.jpg" % (self.photo_id, self.secret)
        elif self.photo_type == 'tumblr':
            # We don't necessarily know that the photo will be a JPEG.  To 
            # be safe, let's just take the path component of the URL and 
            # use that (after removing any slashes).
            tumblr_photo_path = urlparse(self.photo_url)[2].replace('/', '')
            return "tumblr_orig_%s" % (tumblr_photo_path)
        else:
            # ???
            raise Exception

    def _get_cached_original_fn(self):
        """This returns the cached original photo's filename."""
        fn = self._get_cached_original_shortname()
        return "%s/%s" % (config.IMAGE_CACHE_DIR, fn)

    def _get_cached_thumbnail_fn(self):
        if self.photo_type == 'flickr':
            return "%s/flickr_thumb_%s_%s.jpg" % (config.IMAGE_CACHE_DIR, self.photo_id, self.secret)
        elif self.photo_type == 'tumblr':
            # See get_cached_original_fn()
            tumblr_photo_path = urlparse(self.photo_url)[2].replace('/', '')
            return "%s/tumblr_thumb_%s" % (config.IMAGE_CACHE_DIR, tumblr_photo_path)
        else:
            # ???
            raise Exception

    def set_dimensions(self):
        try:
            image = Image.open(self._get_cached_original_fn())
            (self.width, self.height) = image.size
        except IOError:
            raise NonexistentImageError

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
    
    def set_content(self):
        """Creates a content value suitable for using in a feed."""
        try:
            self.content = """<img src="%s" height="%s" width="%s" alt="" /><br />%s""" % (config.BASE_URL + self.cached_url, self.height, self.width, self.summary)
            self.logger.debug("Content: '%s'" % self.content)
        except:
            self.logger.exception("Error occurred while creating content attribute!")
            self.content = ''

def main():
    pass

if __name__ == '__main__':
    main()

