#!/usr/bin/env python
# encoding: utf-8
"""
backwatertest.py

Created by Jacob C. on 2008-02-26.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import unittest
import spider
from spider.source import Source
from spider.weblog import Weblog
from spider.linklog import Linklog
from spider.commentlog import Commentlog
from spider.tumblelog import Tumblelog
from spider.photostream import Photostream
from spider.twitterstatus import TwitterStatus
import publish.sanitizer
import publish.shorten
import publish.typogrify

class SanityTestCases(unittest.TestCase):
    # TODO: Sanity test URLs need to be placed in a data structure like the sources.yaml file
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
            'http://wileywiggins.blogspot.com/feeds/posts/default',
            'http://feeds.feedburner.com/greeninterfaces'
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
        self.url = 'http://example.com/test'
        self.base_url = 'http://chompy.net/lab/backwater/tests/sources/weblog/'
        self.atom_url = self.base_url + 'atom.atom'
        self.rss_url = self.base_url + 'rss.rss'
        self.rdf_url = self.base_url + 'rdf.rdf'
        self.no_title_url = self.base_url + 'no_title.atom'
        self.no_summary_url = self.base_url + 'no_summary.atom'
        self.no_content_url = self.base_url + 'no_content.atom'
        self.author_details_url = self.base_url + 'author_details.atom'
        self.no_author_details_url = self.base_url + 'no_author_details.atom'
        self.multiple_alternate_links_url = self.base_url + 'multple_alternate_links.atom'
        self.related_link_url = self.base_url + 'related_link_url.atom'
        self.via_link_url = self.base_url + 'via_link_url.atom'
        self.comments_url = self.base_url + 'comments_url.rss'
        self.atom_source_url = self.base_url + 'atom_source_url.atom'
    
    def testIsAtom(self):
        """An Atom feed can be detected."""
        w = Weblog('test', 'testy', self.url, self.atom_url)
        w.parse()
        w.normalize()
        for entry in w.entries:
            entry.normalize()
        assert w.atom == True
        
    def testIsNotAtom(self):
        """A non-Atom feed can be detected."""
        w = Weblog('test', 'testy', self.url, self.rss_url)
        w.parse()
        w.normalize()
        for entry in w.entries:
            entry.normalize()
        assert w.atom == False
    
    def testFeedWithMissingEntryLinks(self):
        """Feed items with entry.links missing can be parsed."""
        w = Weblog('test', 'testy', self.url, self.rss_url)
        w.parse()

class TumblelogTestCases(unittest.TestCase):
    def setUp(self):
        pass

class PhotoTestCases(unittest.TestCase):
    def setUp(self):
        pass

class TwitterTestCases(unittest.TestCase):
    def setUp(self):
        self.plain_ol_tweet = """I'm preparing a delicious sandwich!"""
        self.tweet_with_hashtag = """This caprese has changed my life! #inspirationalsalads"""
        self.tweet_with_username = """@mozzarella Are you buffalo or garden variety?"""
        self.tweet_with_username_and_punctuation = """@NuerOb: I am like a pot roast, but better!"""
        self.tweet_with_url = "What an outstanding website! http://chompy.net"
        self.tweet_with_reply = "@lemmycaution What do you love above all?"
        self.tweet_with_retweet = "RT @lemmycaution I refuse to become what you call normal."
        self.tweet_with_the_works = ""
        self.example_account = "setholdmixon"

    def testLinkHashtag(self):
        """Twitter hashtags are automatically linked."""
        expected = """This caprese has changed my life! <a href="http://twitter.com/search?q=%23inspirationalsalads">#inspirationalsalads</a>"""
        result = TwitterStatus.link_hashtags(self.tweet_with_hashtag)
        assert result == expected

    def testLinkUsername(self):
        """Twitter usernames are automatically linked."""
        expected = """@<a href="http://twitter.com/mozzarella/">mozzarella</a> Are you buffalo or garden variety?"""
        result = TwitterStatus.link_users(self.tweet_with_username)
        assert result == expected
        
    def testLinkUsernameWithPunctuation(self):
        """A Twitter username with trailing punctuation can be linked."""
        expected = """@<a href="http://twitter.com/NuerOb/">NuerOb</a>: I am like a pot roast, but better!"""
        result = TwitterStatus.link_users(self.tweet_with_username)
        assert result == expected
    
    def testLinkUrl(self):
        """URLs within tweets are automatically linked."""
        expected = """What an outstanding website! <a href="http://chompy.net">http://chompy.net</a>"""
        # TODO: Finish this test case
    
    def testIgnoreReply(self):
        """Twitter replies can be ignored."""
        self.assertTrue(TwitterStatus.is_reply(self.tweet_with_reply))
    
    def testIgnoreRetweet(self):
        """Twitter retweets, which are annoying, can be ignored."""
        self.assertTrue(TwitterStatus.is_retweet(self.tweet_with_retweet))
    
    def parseTwitterStatus(self):
        """A real-world Twitter status feed can be parsed."""
        name = self.example_account
        owner = self.example_account
        url = "http://twitter.com/" + self.example_account
        t = TwitterStatus(name, owner, url)
        t.parse()

class StripperTestCases(unittest.TestCase):
    def setUp(self):
        self.basic_txt = """<h1>Change <em>alone</em> is unchanging.</h1>"""
        self.plain_txt = "The dead body is useless even as manure."
        self.txt_with_attrs = """Law gives the people a <a href="http://example.com/">single will</a> to obey."""
        self.txt_with_minimized_attrs = """Law gives the people a <option selected>single will</option> to obey."""
        self.txt_with_entities = """<blockquote><p>I&#8217;ve seen Plato&apos;s cups &amp; tables, but not his <i>cupness</i> &amp; <i>tableness</i>.</p></blockquote>"""
        self.style_tag = """The <span style="font-family: 'Comic Sans';">same road</span> goes both up and down."""
        self.script_tag = """Men are not intellligent. <script type="text/javascript">alert('Not enough and too much.');</script> The gods are intelligent."""
        self.script_url = """The <a href="javascript:alert('boo');">untrained mind</a> shivers with excitement at everything it hears."""
        self.self_closed_html_tag = """To God all is beautiful, good, and as it should be.<br> Man must see things as either good or bad."""
        self.self_closed_xhtml_tag = """To God all is beautiful, good, and as it should be.<br /> Man must see things as either good or bad."""
        self.nested_tags = """Having cut, <a href="http://example.com"><b>burned</b> and <font style="color: #CCC;">poisoned</font></a> the sick, the doctor then submits <strong>his bill</strong>."""
        self.unbalanced_tags = """<h1>Extinguish <q>pride <b>as</q> quickly</b> as you would a fire."""
        self.unknown_tags = """Law gives the people a <turkey gobble="http://example.com/">single will</turkey> to obey."""
        
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
   
    def testStripTagsWithMinimizedAttributes(self):
        """HTML tags containing minimized attributes are stripped."""
        result = publish.sanitizer.strip(self.txt_with_minimized_attrs)
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

    def testStripUnknownTags(self):
        """Unknown markup is stripped."""
        result = publish.sanitizer.strip(self.unknown_tags)
        assert result == """Law gives the people a single will to obey."""

class TagSubstitutionTestCases(unittest.TestCase):
    def setUp(self):
        self.one_paragraph = "<p>The falcon cannot hear the falconer.</p>"
        self.two_paragraphs = "<p>A doll in the doll-maker's house</p><p>Looks at the cradle and bawls</p>"
        self.mixed_blocks = """<p>Cuchulain has killed kings</p><h1>Kings and sons of kings</h1><p>Dragons out of the water</p>"""
        self.with_newline = """<p>Witches that steal the milk</p>\n<p>Fomor that steal the children</p>"""
        self.h1 = """<h1>Sailing to Byzantium</h1>"""
        self.h1_with_attr = """<h1 id="ct_130213948">Celtic Twilight</h1>"""
        self.h1_with_nested_anchor = """<h1><a href="http://example.com/">Easter 1918</a></h1>"""
    
    def testHeadingToBold(self):
        """Block-level <h1> tags are replaced with inline <b> tags."""
        result = publish.sanitizer.heading_to_bold(self.h1)
        assert result == """<b>Sailing to Byzantium</b>"""
        
    def testHeadingWithAttributesToBold(self):
        """<h1> tags with attributes are replaced with <b> tags."""
        result = publish.sanitizer.heading_to_bold(self.h1_with_attr)
        assert result == """<b>Celtic Twilight</b>"""
        
    def testHeadingWithNestedAnchorToBold(self):
        """<h1> tags with nested anchors are replaced with <b> tags."""
        result = publish.sanitizer.heading_to_bold(self.h1_with_nested_anchor)
        assert result == """<b><a href="http://example.com/">Easter 1918</a></b>"""
    
    def testBlocktoBrWithOneParagraph(self):
        """block_to_break() strips a lone <p> tag."""
        result = publish.sanitizer.block_to_break(self.one_paragraph)
        print result
        assert result == """The falcon cannot hear the falconer."""

    def testBlockToBreakWithTwoParagraphs(self):
        """block_to_break() strips two <p> tags and places two <br>s between them."""
        result = publish.sanitizer.block_to_break(self.two_paragraphs)
        print result
        assert result == """A doll in the doll-maker's house<br /><br />Looks at the cradle and bawls"""

    def testBlockToBreakWithMixedBlocks(self):
        """block_to_break() deals correctly with mixed block tags."""
        result = publish.sanitizer.block_to_break(self.mixed_blocks)
        print result
        assert result == """Cuchulain has killed kings<br /><br />Kings and sons of kings<br /><br />Dragons out of the water"""

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
        self.whitelisted_tags_in_blacklisted_tags = """Having cut, <font style="color: red;">burned and <em>poisoned</em></font> the sick, the doctor then submits his bill."""
        self.unbalanced_tags = """<h1>Extinguish <q>pride <b>as</q> quickly</b> as you would a fire."""
        self.ampersands = """To God all is beautiful, good, & as it should be."""
        self.unknown_tags = """Law gives the people a <turkey gobble="http://example.com/">single will</turkey> to obey."""

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

    def testSanitizeWhitelistedTagsInBlacklistedTags(self):
        """Whitelisted tags nested in non-whitelisted tags are preserved."""
        result = publish.sanitizer.sanitize(self.whitelisted_tags_in_blacklisted_tags)
        assert result == """Having cut, burned and <em>poisoned</em> the sick, the doctor then submits his bill."""
        
    def testSanitizeUnbalancedTags(self):
        """Unbalanced HTML tags are sanitized and balanced."""
        result = publish.sanitizer.sanitize(self.unbalanced_tags)
        assert result == """Extinguish <q>pride <b>as</b></q> quickly as you would a fire.""" 

    def testSanitizeAmpersands(self):
        """Ampersands are not encoded by the sanitizer."""
        result = publish.sanitizer.sanitize(self.ampersands)
        assert result == self.ampersands

    def testSanitizeUnknownTags(self):
        """Unknown markup is removed by the sanitizer."""
        result = publish.sanitizer.sanitize(self.unknown_tags)
        assert result == """Law gives the people a single will to obey."""

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
    def testTypogrify(self):
        """The typogrify() function prepares text for fancy CSS."""
        result = publish.typogrify.typogrify('<h2>"Jayhawks" & KU fans act extremely obnoxiously</h2>')
        assert result == '<h2><span class="dquo">&#8220;</span>Jayhawks&#8221; <span class="amp">&amp;</span> <span class="caps">KU</span> fans act extremely&#160;obnoxiously</h2>'

    def testItsPowerLevelIs9000(self):
        """Dakota's bizarre phrase "IT'S POWER LEVEL IS 9000" must survive Typogrify."""
        result = publish.typogrify.typogrify("IT'S POWER LEVEL IS 9000")
        assert result == """<span class="caps">IT</span>&#8217;S <span class="caps">POWER</span> <span class="caps">LEVEL</span> <span class="caps">IS</span>&#160;9000"""

class TypogrifyAmpTestCases(unittest.TestCase):
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

class TypogrifyCapsTestCases(unittest.TestCase):
    def testWrapsCaps(self):
        """Capital letters are typogrified."""
        result = publish.typogrify.caps("A message from KU")
        assert result == 'A message from <span class="caps">KU</span>'

    def testDontWrapPre(self):
        """Capital letters in a <pre> block are not typogrified."""
        result = publish.typogrify.caps("<PRE>CAPS</pre> more CAPS")
        assert result == '<PRE>CAPS</pre> more <span class="caps">CAPS</span>'

    def testWrapCapsWithNumbers(self):
        """Capital letters with numbers are typogrified."""
        result = publish.typogrify.caps("A message from 2KU2 with digits")
        assert result == 'A message from <span class="caps">2KU2</span> with digits'

    def testDottedCapsWithSpaces(self):
        """The spaces following dotted caps are not typogrified."""
        result = publish.typogrify.caps("Dotted caps followed by spaces should never include them in the wrap D.O.T.   like so.")
        assert result == 'Dotted caps followed by spaces should never include them in the wrap <span class="caps">D.O.T.</span>  like so.'

    def testCapsNestedInTags(self):
        """Capital letters nested in other tags are typogrified."""
        result = publish.typogrify.caps("<i>D.O.T.</i>HE34T<b>RFID</b>")
        assert result == '<i><span class="caps">D.O.T.</span></i><span class="caps">HE34T</span><b><span class="caps">RFID</span></b>'

    def testCapsPossessivesAndContractions(self):
        """Capital letters in possessives and contractions are typogrified."""
        result = publish.typogrify.caps("JACKIE'S DRUNKEN BOXING CAN'T BEAT MY KUNG FU")
        assert result == """<span class="caps">JACKIE'S</span> <span class="caps">DRUNKEN</span> <span class="caps">BOXING</span> <span class="caps">CAN'T</span> <span class="caps">BEAT</span> <span class="caps">MY</span> <span class="caps">KUNG</span> <span class="caps">FU</span>"""

class TypogrifyInitialQuotesTestCases(unittest.TestCase):
    def testInitialDoubleQuotes(self):
        """Initial double quotes are typogrified."""
        result = publish.typogrify.initial_quotes('"With primes"')
        assert result == '<span class="dquo">"</span>With primes"'

    def testInitialSingleQuotes(self):
        """Initial single quotes are typogrified."""
        result = publish.typogrify.initial_quotes("'With single primes'")
        assert result == """<span class="quo">'</span>With single primes'"""

    def testInitialDoubleQuotesWithLink(self):
        """Initial double quotes in a link are typogrified."""
        result = publish.typogrify.initial_quotes('<a href="#">"With primes and a link"</a>')
        assert result == '<a href="#"><span class="dquo">"</span>With primes and a link"</a>'

    def testInitialSmartQuotes(self):
        """Initial smart quotes are typogrified."""
        result = publish.typogrify.initial_quotes('&#8220;With smartypanted quotes&#8221;')
        assert result == '<span class="dquo">&#8220;</span>With smartypanted quotes&#8221;'

class TypogrifySmartypantsTestCases(unittest.TestCase):
    def testSmartypants(self):
        """ASCII punctuation is converted to 'smart' punctuation."""
        result = publish.typogrify.smartypants('The "Green" man')
        assert result == 'The &#8220;Green&#8221; man'
        
    def testItsPowerLevelIs9000(self):
        """Dakota's bizarre phrase "IT'S POWER LEVEL IS 9000" must survive SmartyPants."""
        result = publish.typogrify.smartypants("IT'S POWER LEVEL IS 9000")
        assert result == "IT&#8217;S POWER LEVEL IS 9000"

class TypogrifyWidontTestCases(unittest.TestCase):
    def testWidont(self):
        """Textual widows are prevented."""
        result = publish.typogrify.widont('A very simple test')
        assert result == 'A very simple&#160;test'

    def testWidontSingleWord(self):
        """Widont processing is skipped for single-word strings."""
        result = publish.typogrify.widont('Test')
        assert result == 'Test'

    def testWidontInitialSpace(self):
        """Widont processing is skipped for single words preceded by a space."""
        result = publish.typogrify.widont(' Test')
        assert result == ' Test'

    def testWidontSingleWordInTags(self):
        """Widont processing is skipped for single-word strings in markup."""
        result = publish.typogrify.widont('<ul><li>Test</p></li><ul>')
        assert result == '<ul><li>Test</p></li><ul>'

    def testWidont04(self):
        """Describe what the test does here."""
        result = publish.typogrify.widont('<ul><li> Test</p></li><ul>')
        assert result == '<ul><li> Test</p></li><ul>'

    def testWidont05(self):
        """Describe what the test does here."""
        result = publish.typogrify.widont('<p>In a couple of paragraphs</p><p>paragraph two</p>')
        assert result == '<p>In a couple of&#160;paragraphs</p><p>paragraph&#160;two</p>'

    def testWidont06(self):
        """Describe what the test does here."""
        result = publish.typogrify.widont('<h1><a href="#">In a link inside a heading</i> </a></h1>')
        assert result == '<h1><a href="#">In a link inside a&#160;heading</i> </a></h1>'

    def testWidont07(self):
        """Describe what the test does here."""
        result = publish.typogrify.widont('<h1><a href="#">In a link</a> followed by other text</h1>')
        assert result == '<h1><a href="#">In a link</a> followed by other&#160;text</h1>'

    def testWidont08(self):
        """Describe what the test does here."""
        result = publish.typogrify.widont('<h1><a href="#"></a></h1>')
        assert result == '<h1><a href="#"></a></h1>'

    def testWidont09(self):
        """Describe what the test does here."""
        result = publish.typogrify.widont('<div>Divs get no love!</div>')
        assert result == '<div>Divs get no love!</div>'

    def testWidont10(self):
        """Describe what the test does here."""
        result = publish.typogrify.widont('<pre>Neither do PREs</pre>')
        assert result == '<pre>Neither do PREs</pre>'

    def testWidont11(self):
        """Describe what the test does here."""
        result = publish.typogrify.widont('<div><p>But divs with paragraphs do!</p></div>')
        assert result == '<div><p>But divs with paragraphs&#160;do!</p></div>'

if __name__ == '__main__':
    unittest.main()
