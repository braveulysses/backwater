#!/usr/bin/env python
# encoding: utf-8
"""
backwatertest.py

Created by Jacob C. on 2008-02-26.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import unittest
import publish.sanitizer
import publish.shorten
import publish.typogrify

class SanityTestCases(unittest.TestCase):
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

class FeedTestCases(unittest.TestCase):
    def setUp(self):
        pass
    
    def isAtom(self):
        """An Atom feed can be detected."""
        pass
        
    def isNotAtom(self):
        """A non-Atom feed can be detected."""
        pass

class TumblelogTestCases(unittest.TestCase):
    def setUp(self):
        pass

class PhotoTestCases(unittest.TestCase):
    def setUp(self):
        pass

class SanitizerTestCases(unittest.TestCase):
    def setUp(self):
        pass

class ShortenTestCases(unittest.TestCase):
    def setUp(self):
        self.txt = "there are five new tomato plants, all in new places; where they were all on the west row last year, now they're all on the south, with one in the west. we also planted new eggplant, salad burnet, flax, basil, and artichoke. the artichoke is on the opposite corner as last year, and the eggplant has moved south. they say you have to plan for succession planting, but when you've got the right friends, it really makes these things far simpler."
        self.short_txt = "Why do you do me like you do?"
        self.really_short_txt = "I wanna tell you one thing."
        
    def testCountWords(self):
        """The number of words in a string can be correctly counted."""
        count = publish.shorten.wc(self.txt)
        assert count == 81

    def testShortenText(self):
        """A string can be truncated to an arbitrary number of words."""
        result = publish.shorten.shorten(self.txt, 10)
        print result
        assert result == 'there are five new tomato plants, all in new places;&#8230;'

    def testShortenShortTest(self):
        """Text that is right at the word limit is not shortened."""
        result = publish.shorten.shorten(self.short_txt, 8)
        assert result == self.short_txt

    def testShortenReallyShortTest(self):
        """Text that is under the word limit is not shortened."""
        result = publish.shorten.shorten(self.really_short_txt, 7)
        assert result == self.really_short_txt

class TypogrifyTestCases(unittest.TestCase):
    def setUp(self):
        pass
    
    def testWrapAmp(self):
        """Ampersands are entity-encoded and wrapped in the 'amp' class."""
        txt = 'One & two'
        result = publish.typogrify.amp(txt)
        assert result == 'One <span class="amp">&amp;</span> two'

    def testWrapEncodedAmp(self):
        """Ampersands that are already entity-encoded are not double-encoded."""
        txt = 'One &amp; two'
        result = publish.typogrify.amp(txt)
        assert result == 'One <span class="amp">&amp;</span> two'

    def testWrapNumericEncodedAmp(self):
        """Ampersands that are already numeric entity-encoded are not double-encoded."""
        txt = 'One &#38; two'
        result = publish.typogrify.amp(txt)
        assert result == 'One <span class="amp">&amp;</span> two'

    def testWrapAmpWithNbsp(self):
        """Ampersands that are surrounded by '&nbsp;' are properly handled."""
        txt = 'One&nbsp;&amp;&nbsp;two'
        result = publish.typogrify.amp(txt)
        assert result == 'One&nbsp;<span class="amp">&amp;</span>&nbsp;two'

    def testAlreadyWrappedAmp(self):
        """Ampersands that have already been processed aren't double-processed."""
        txt = 'One <span class="amp">&amp;</span> two'
        result = publish.typogrify.amp(txt)
        assert result == 'One <span class="amp">&amp;</span> two'

    def testAmpEncodedInUrl(self):
        """Ampersands already encoded in a URL are preserved."""
        txt = '&ldquo;this&rdquo; & <a href="/?that&amp;test">that</a>'
        result = publish.typogrify.amp(txt)
        assert result == '&ldquo;this&rdquo; <span class="amp">&amp;</span> <a href="/?that&amp;test">that</a>'

    def testAmpInAttribute(self):
        """Ampersands in attribute values are ignored."""
        txt = '<link href="xyz.html" title="One & Two">xyz</link>'
        result = publish.typogrify.amp(txt)
        assert result == '<link href="xyz.html" title="One & Two">xyz</link>'

if __name__ == '__main__':
    unittest.main()