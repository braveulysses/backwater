#!/usr/bin/env python
# encoding: utf-8
"""
photostream.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import flickrapi
import logging
import config
from source import Source
from entries import Photo

module_logger = logging.getLogger("backwater.photostream")

class Photostream(Source):
    def __init__(self, name, owner, url, flickr_id):
        super(Photostream, self).__init__(name, owner, url)
        self.logger = logging.getLogger("backwater.photostream.Photostream")
        self.type = 'photostream'
        self.entry_type = 'photo'
        self.flickr_id = flickr_id

    def parse(self):
        """Get recent photos from a photostream."""
        self.logger.debug("Contacting Flickr Services")
        flickr = flickrapi.FlickrAPI(config.FLICKR_KEY, format='etree')
        extras = 'date_upload,owner_name'
        self.logger.info("Getting photos for %s" % self.owner)
        photos = flickr.people_getPublicPhotos(user_id=self.flickr_id, extras=extras)
        for photo in photos:
            e = Photo()
            p = photo.find('photo')
            e.title = p.get('title')
            self.logger.info("Photo title: '%s'" % e.title)
            e.id = p.get('id')
            e.secret = p.get('secret')
            e.server = p.get('server')
            e.url = 'http://static.flickr.com/%s/%s_%s.jpg' % (e.server, e.id, e.secret)
            self.logger.debug("Photo static URL: '%s'" % e.url)
            e.photostream_url = 'http://www.flickr.com/photos/%s/%s/' % (self.flickr_id, e.id)
            self.logger.debug("Photo Flickr URL: '%s'" % e.photostream_url)

def main():
    pass

if __name__ == '__main__':
    main()

