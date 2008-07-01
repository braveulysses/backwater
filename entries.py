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

module_logger = logging.getLogger("backwater.entries")

class Entry(object):
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
        self.photostream_url = ''

    def cache():
        pass

def main():
    pass

if __name__ == '__main__':
    main()

