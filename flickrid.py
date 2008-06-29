#!/usr/bin/env python
# encoding: utf-8
"""
flickrid.py
Utility to get the Flickr ID from a Flickr username.

Created by Jacob C. on 2008-06-29.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import sys
import getopt
import flickrapi
import config


help_message = '''
Usage: python %s USERNAME
Gets the Flickr ID of USERNAME.
''' % sys.argv[0]


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def get_flickr_id(username):
    flickr = flickrapi.FlickrAPI(config.FLICKR_KEY, format='etree')
    user = flickr.people_findByUsername(username=username)
    return user.find('user').get('nsid')

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", [ "help" ])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option in ("-h", "--help"):
                raise Usage(help_message)
        
        try:
            username = argv[1]
        except IndexError, msg:
            raise Usage(help_message)
        
        try:
            id = get_flickr_id(username)
            print id
        except flickrapi.exceptions.FlickrError, msg:
            print >> sys.stderr, "Error getting Flickr ID: '%s'" % msg
            print >> sys.stderr
            return 1
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        return 2


if __name__ == "__main__":
    sys.exit(main())
