#!/usr/bin/env python
# encoding: utf-8
"""
entries.py

Created by Jacob C. on 2008-06-26.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

class Entry(object):
    def __init__(self):
        super(Entry, self).__init__()
        self.title = ''
        self.author = ''
        self.summary = ''
        self.content = ''
        self.url = ''
        self.date = None
        self.published = None
        self.created = None
        self.updated = None

class Post(Entry):
    def __init__(self):
        super(Post, self).__init__()
        self.comments = None
        self.enclosures = None
        self.tags = None
        self.via = None

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

def main():
    pass

if __name__ == '__main__':
    main()

