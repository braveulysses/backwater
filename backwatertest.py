#!/usr/bin/env python
# encoding: utf-8
"""
backwatertest.py

Created by Jacob C. on 2008-02-26.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import unittest

class SanityTestCase(unittest.TestCase):
    def setUp(self):
        self.live_urls = (
            'http://chompy.net/blogs/jacob/feeds/index.atom',
            'http://chompy.net/blogs/pogo/atom.xml',
            'http://chompy.net/blogs/nathalie/atom.xml',
            'http://palcontent.blogspot.com/feeds/posts/default',
            'http://hoolifan.blogspot.com/feeds/posts/default',
            'http://bubblegumdamage.blogspot.com/feeds/posts/default',
            'http://savagepencil.typepad.com/charlieletters/index.rdf',
            'http://savagepencil.typepad.com/confessions/index.rdf',
            'http://headcrab.org/feed/atom/',
            'http://benkerishan.blogspot.com/feeds/posts/default',
            'http://www.tbray.org/ongoing/ongoing.atom',
            'http://wileywiggins.blogspot.com/feeds/posts/default'
        )
        self.test_urls = (
            'http://chompy.net/lab/backwater/tests/sanity/remakeremodel.xml',
            'http://chompy.net/lab/backwater/tests/sanity/darkentries.xml',
            'http://chompy.net/lab/backwater/tests/sanity/peenywally.xml',
            'http://chompy.net/lab/backwater/tests/sanity/tigerpounces.xml',
            'http://chompy.net/lab/backwater/tests/sanity/greencandle.xml',
            'http://chompy.net/lab/backwater/tests/sanity/garbage.xml',
            'http://chompy.net/lab/backwater/tests/sanity/bubblegumdamage.xml',
            'http://chompy.net/lab/backwater/tests/sanity/charlieletters.xml',
            'http://chompy.net/lab/backwater/tests/sanity/confessions.xml',
            'http://chompy.net/lab/backwater/tests/sanity/headcrab.xml',
            'http://chompy.net/lab/backwater/tests/sanity/arabic.xml',
            'http://chompy.net/lab/backwater/tests/sanity/ongoing.xml',
            'http://chompy.net/lab/backwater/tests/sanity/newsofthedead.xml'
        )

class FeedTestCase(unittest.TestCase):
    def setUp(self):
        pass

class TumblelogTestCase(unittest.TestCase):
    def setUp(self):
        pass

class PhotoTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
if __name__ == '__main__':
    unittest.main()