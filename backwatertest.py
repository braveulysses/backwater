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

class StripperTestCases(unittest.TestCase):
    def setUp(self):
        self.basic_txt = """<h1>Change <em>alone</em> is unchanging.</h1>"""
        self.plain_txt = "The dead body is useless even as manure."
        self.txt_with_attrs = """Law gives the people a <a href="http://example.com/">single will</a> to obey."""
        self.txt_with_entities = """<blockquote><p>I&#8217;ve seen Plato&apos;s cups &amp; tables, but not his <i>cupness</i> &amp; <i>tableness</i>.</p></blockquote>"""
        self.style_tag = """The <span style="font-family: 'Comic Sans';">same road</span> goes both up and down."""
        self.script_tag = """Men are not intellligent. <script type="text/javascript">alert('Not enough and too much.');</script> The gods are intelligent."""
        self.script_url = """The <a href="javascript:alert('boo');">untrained mind</a> shivers with excitement at everything it hears."""
        self.self_closed_html_tag = """To God all is beautiful, good, and as it should be.<br> Man must see things as either good or bad."""
        self.self_closed_xhtml_tag = """To God all is beautiful, good, and as it should be.<br /> Man must see things as either good or bad."""
        self.nested_tags = """Having cut, <a href="http://example.com"><b>burned</b> and <font style="color: #CCC;">poisoned</font></a> the sick, the doctor then submits <strong>his bill</strong>."""
        self.unbalanced_tags = """<h1>Extinguish <q>pride <b>as</q> quickly</b> as you would a fire."""
        
    def testStripTags(self):
        """HTML tags are stripped from text."""
        result = publish.sanitizer.strip(self.basic_txt)
        assert result == 'Change alone is unchanging.'
    
    def testStripPlainText(self):
        """HTML stripper leaves plain text as is."""
        result = publish.sanitizer.strip(self.plain_txt)
        assert result == self.plain_txt
    
    def testStripTagsWithAttributes(self):
        """HTML tags containing attributes are stripped."""
        result = publish.sanitizer.strip(self.txt_with_attrs)
        assert result == "Law gives the people a single will to obey."
    
    def testStripTagsWIthEntities(self):
        """HTML entities are converted to Unicode characters by the HTML stripper."""
        result = publish.sanitizer.strip(self.txt_with_entities)
        assert result == "I’ve seen Plato's cups & tables, but not his cupness & tableness."
    
    def testStripStyleTags(self):
        """HTML <style> tags are stripped."""
        result = publish.sanitizer.strip(self.style_tag)
        assert result == "The same road goes both up and down."
    
    def testStripScriptTags(self):
        """HTML <script> tags are stripped."""
        result = publish.sanitizer.strip(self.script_tag)
        assert result == "Men are not intellligent. alert('Not enough and too much.'); The gods are intelligent."
    
    def testStripSelfClosedHtmlTags(self):
        """Self-closed tags such as <br> are stripped."""
        result = publish.sanitizer.strip(self.self_closed_html_tag)
        assert result == """To God all is beautiful, good, and as it should be. Man must see things as either good or bad."""
        
    def testStripSelfClosedXhtmlTags(self):
        """Self-closed tags such as <br /> are stripped."""
        result = publish.sanitizer.strip(self.self_closed_xhtml_tag)
        assert result == """To God all is beautiful, good, and as it should be. Man must see things as either good or bad."""
        
    def testStripNestedTags(self):
        """Nested HTML tags are stripped."""
        result = publish.sanitizer.strip(self.nested_tags)
        assert result == """Having cut, burned and poisoned the sick, the doctor then submits his bill."""

    def testStripUnbalancedTags(self):
        """Unbalanced HTML tags are stripped."""
        result = publish.sanitizer.strip(self.unbalanced_tags)
        assert result == "Extinguish pride as quickly as you would a fire."

class SanitizeTestCases(unittest.TestCase):
    def setUp(self):
        # FIXME: The default whitelist is assumed. 
        # It would be better to specify the whitelist.
        self.basic_txt = """<h1>Change <em>alone</em> is unchanging."""
        self.plain_txt = "The dead body is useless even as manure."
        self.txt_with_attrs = """Law gives the people a <a href="http://example.com/">single will</a> to obey."""
        self.txt_with_entities = """<blockquote><p>I&#8217;ve seen Plato&apos;s cups &amp; tables, but not his <i>cupness</i> &amp; <i>tableness</i>.</p></blockquote>"""
        self.style_tag = """The <span style="font-family: 'Comic Sans';">same road</span> goes both up and down."""
        self.script_tag = """Men are not intellligent. <script type="text/javascript">alert('Not enough and too much.');</script> The gods are intelligent."""
        self.script_url = """The <a href="javascript:alert('boo');">untrained mind</a> shivers with excitement at everything it hears."""
        self.html_br = """To God all is beautiful, good, and as it should be.<br> Man must see things as either good or bad."""
        self.html_hr = """To God all is beautiful, good, and as it should be.<hr> Man must see things as either good or bad."""
        self.xhtml_br = """To God all is beautiful, good, and as it should be.<br /> Man must see things as either good or bad."""
        self.xhtml_hr = """To God all is beautiful, good, and as it should be.<hr /> Man must see things as either good or bad."""
        self.nested_tags = """Having cut, <a href="http://example.com"><b>burned</b> and <font style="color: #CCC;">poisoned</font></a> the sick, the doctor then submits <strong>his bill</strong>."""
        self.unbalanced_tags = """<h1>Extinguish <q>pride <b>as</q> quickly</b> as you would a fire."""

    def testSanitizedTags(self):
        """HTML tags are sanitized using a whitelist."""
        result = publish.sanitizer.sanitize(self.basic_txt)
        assert result == 'Change <em>alone</em> is unchanging.'

    def testSanitizePlainText(self):
        """HTML sanitizer leaves plain text as is."""
        result = publish.sanitizer.sanitize(self.plain_txt)
        assert result == self.plain_txt

    def testSanitizeLinks(self):
        """Links with safe URLs are preserved by the sanitizer."""
        result = publish.sanitizer.sanitize(self.txt_with_attrs)
        assert result == """Law gives the people a <a href="http://example.com/">single will</a> to obey."""

    def testSanitizeTagsWIthEntities(self):
        """HTML entities are preserved by the HTML sanitizer and not double-encoded."""
        result = publish.sanitizer.sanitize(self.txt_with_entities)
        assert result == """<blockquote><p>I&#8217;ve seen Plato&apos;s cups &amp; tables, but not his <i>cupness</i> &amp; <i>tableness</i>.</p></blockquote>"""

    def testSanitizeStyleTags(self):
        """HTML <style> tags are stripped by the sanitizer."""
        result = publish.sanitizer.sanitize(self.style_tag)
        assert result == "The same road goes both up and down."

    def testSanitizeScriptTags(self):
        """HTML <script> tags are stripped by the sanitizer."""
        result = publish.sanitizer.sanitize(self.script_tag)
        assert result == "Men are not intellligent.  The gods are intelligent."

    def testSanitizeHtmlBrs(self):
        """Self-closed tags such as <br> are converted to <br /> by the sanitizer."""
        result = publish.sanitizer.sanitize(self.html_br)
        assert result == """To God all is beautiful, good, and as it should be.<br /> Man must see things as either good or bad."""

    def testSanitizeHtmlHrs(self):
        """Self-closed tags such as <hr> are removed by the sanitizer."""
        result = publish.sanitizer.sanitize(self.html_hr)
        assert result == """To God all is beautiful, good, and as it should be. Man must see things as either good or bad."""

    def testSanitizeXhtmlBrs(self):
        """Self-closed tags such as <br /> are preserved by the sanitizer."""
        result = publish.sanitizer.sanitize(self.xhtml_br)
        assert result == """To God all is beautiful, good, and as it should be.<br /> Man must see things as either good or bad."""
        
    def testSanitizeXhtmlHrs(self):
        """Self-closed tags such as <hr /> are removed by the sanitizer."""
        result = publish.sanitizer.sanitize(self.xhtml_hr)
        assert result == """To God all is beautiful, good, and as it should be. Man must see things as either good or bad."""

    def testSanitizeNestedTags(self):
        """Nested HTML tags are sanitized."""
        result = publish.sanitizer.sanitize(self.nested_tags)
        assert result == """Having cut, <a href="http://example.com"><b>burned</b> and poisoned</a> the sick, the doctor then submits <strong>his bill</strong>."""
        
    def testSanitizeUnbalancedTags(self):
        """Unbalanced HTML tags are sanitized and balanced."""
        result = publish.sanitizer.sanitize(self.unbalanced_tags)
        assert result == """Extinguish <q>pride <b>as</b></q> quickly as you would a fire.""" 

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