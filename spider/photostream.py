#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
photostream.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2010 Spaceship No Future. All rights reserved.
"""

import datetime
import flickrapi
import logging
import config
from feedparser import _parse_date as parse_date
from flickrapi.exceptions import FlickrError
from source import Source
from entries import Photo

module_logger = logging.getLogger("backwater.photostream")

SAFESEARCH_SAFE = 1
SAFESEARCH_MODERATE = 2
SAFESEARCH_RESTRICTED = 3

class Photostream(Source):
    def __init__(self, name, owner, url, flickr_id):
        super(Photostream, self).__init__(name, owner, url)
        self.logger = logging.getLogger("backwater.photostream.Photostream")
        self.type = 'photostream'
        self.flickr_id = flickr_id

    def parse(self):
        """Gets recent photos from a photostream, caches and thumbnails them."""
        self.logger.debug("Contacting Flickr Services")
        # Using flickrapi's 'etree' options requires ElementTree, 
        # which is standard with Python 2.5, but a separate install with 
        # Python 2.4.  The flickrapi module must also be patched 
        # using 'patches/flickrapi.patch' when using Python 2.4.
        try:
            flickr = flickrapi.FlickrAPI(config.FLICKR_KEY, format='etree')
            extras = 'date_upload,date_taken,last_update,owner_name,media,tags,license'
            self.logger.info("Getting photos for %s" % self.owner)
            photos = flickr.people_getPublicPhotos(
                        user_id=self.flickr_id, 
                        safe_search=SAFESEARCH_RESTRICTED, 
                        extras=extras
            )
            for photo in photos:
                e = Photo()
                e.photo_type = 'flickr'
                e.source.name = self.name
                e.source.url = self.url
                # This only gets the most recent photo, which is really 
                # a bug, but I like this behavior.  Too many photos 
                # clutter things up.
                p = photo.find('photo')
                #if p.get('media') == 'video':
                #    self.logger.info("Skipping Flickr video")
                #    continue
                e.title = p.get('title', 'untitled')
                if e.title.strip() == '':
                    e.title = 'untitled'
                self.logger.info("Photo title: '%s'" % e.title)
                e.photo_id = p.get('id')
                e.farm_id = p.get('farm')
                e.secret = p.get('secret')
                e.server = p.get('server')
                e.photo_url = e._get_flickr_photo_url(
                    e.farm_id, 
                    e.server, 
                    e.photo_id, 
                    e.secret
                )
                self.logger.debug("Photo image URL: '%s'" % e.photo_url)
                e.url = e._get_flickr_url(self.flickr_id, e.photo_id)
                e.cached_url = config.IMAGES_URL + '/' + e._get_cached_original_shortname()
                self.logger.debug("Photo Flickr page URL: '%s'" % e.url)
                e.cache()
                e.set_dimensions()
                e.date = p.get('dateupload')
                e.date_parsed = datetime.datetime.utcfromtimestamp(float(e.date)).timetuple()
                e.published = e.date
                e.published_parsed = e.date_parsed
                e.created = p.get('datetaken', e.date)
                if e.created == e.date:
                    e.created_parsed = e.date_parsed
                else:
                    e.created_parsed = parse_date(e.created)
                e.updated = p.get('lastupdate', e.date)
                e.updated_parsed = datetime.datetime.utcfromtimestamp(float(e.updated)).timetuple()
                # Okay, now get the detailed photo info
                self.logger.debug("Making photos.getInfo API call...")
                photo_info = flickr.photos_getInfo(photo_id=e.photo_id, secret=e.secret)
                e.summary = photo_info.find('photo').find('description').text
                if e.summary is None:
                    e.summary = ''
                e.author = photo_info.find('photo').find('owner').get('realname')
                if e.author == '':
                    e.author = self.owner
                e.set_content()
                self.entries.append(e)
        except FlickrError, err:
            self.logger.exception("Flickr API error: '%s'" % err)

def main():
    pass

if __name__ == '__main__':
    main()

