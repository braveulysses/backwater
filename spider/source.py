#!/usr/bin/env python
# encoding: utf-8
"""
source.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import logging
import config
from feedparser import _parse_date as parse_date

module_logger = logging.getLogger("backwater.source")

def source_string(name, type, owner, url):
    return """%s
  Type: %s
  Owner: %s
  URL: %s""" % (name, type, owner, url)

class Source(object):
    """Generic Source object from which weblogs, tumblelogs, etc. descend."""
    def __init__(self, name, owner, url):
        super(Source, self).__init__()
        self.logger = logging.getLogger("backwater.source.Source")
        self.type = 'source'
        # Entry type corresponds to the classes defined in entries.py
        self.entry_type = None
        # This needs to unique; if a unique id is not provided, make one
        self.id = None
        # Name: AKA title
        self.name = name
        # Owner: AKA author
        self.owner = owner
        self.generator = None
        self.url = url
        self.updated = None
        self.updated_parsed = None
        self.rights = None
        self.entries = []
        self.http_content = None
        self.http_response = None

    def __str__(self):
        return source_string(self.name, self.type, self.owner, self.url)

    def parse(self):
        """This is a kind of abstract method that does nothing.  Intended to 
        be defined by child objects and called when parsing feeds or other 
        data sources."""
        pass

    def normalize(self):
        """Checks that all attribute values are in order so that the source 
        can be used in an Atom feed."""
        if self.id is None:
            # TODO: generate unique ID
            pass
        if len(self.entries) > 0:
            if self.updated is None:
                self.updated = self.entries[0].updated
            if self.updated_parsed is None:
                self.updated_parsed = parse_date(self.updated)

def main():
    pass

if __name__ == '__main__':
    main()

