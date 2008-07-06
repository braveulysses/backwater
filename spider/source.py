#!/usr/bin/env python
# encoding: utf-8
"""
source.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import logging
import config

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
        self.url = url
        # TODO: borrow or import date parsing logic from feedparser
        self.updated = None
        self.updated_parsed = None
        self.entries = []
        self.http_content = None
        self.http_response = None
        # TODO: support Atom source element:
        # http://www.atomenabled.org/developers/syndication/atom-format-spec.php#element.source

    def __str__(self):
        return source_string(self.name, self.type, self.owner, self.url)

    def parse(self):
        """This is a kind of abstract method that does nothing.  Intended to be
        defined by child objects and called when parsing feeds or other data sources."""
        pass

def main():
	pass

if __name__ == '__main__':
	main()

