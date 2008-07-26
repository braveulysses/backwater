#!/usr/bin/env python
# encoding: utf-8
"""
sanitizer.py

Created by Jacob C. on 2008-07-04.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from xml.sax.saxutils import escape

def fix_amp_encoding(txt):
    """Fixes the double encoding that can occur when a string containing named or numeric entities are passed through a typical entity escaping function."""
    fixamps = re.compile('&amp;((#\w+;)|(amp;)|(lt;)|(gt;)|(ldquo;)|(rdquo;)|(lsquo;)|(rsquo;)|(quot;))')
    txt = fixamps.sub(r'&\g<1>', txt)
    return txt

def escape_xml(txt):
    """Simple escaping; replaces '"', '<', '>', and '&'."""
    entities = {'"': '&quot;'}
    txt = escape(txt, entities)
    txt = fix_amp_encoding(txt)
    return txt

def escape_amps_only(txt):
    """Only escapes ampersands. 
    
    Useful because we're allowing HTML, and thus '<' and '>'."""
    txt = txt.replace('&', '&amp;')
    txt = fix_amp_encoding(txt)
    return txt
  
def sanitize(untrusted_html):
    """Strips dangerous tags and attributes from HTML.
    
    Based on the work of Tom Insam:
    http://jerakeen.org/blog/2008/05/sanitizing-comments-with-python/
    
    The big flaw with this function is that non-whitelisted tags are 
    replaced as bare <span> tags.  The better alternative is to remove 
    the tag from the tree and replace it with its children.  But that's 
    really hard.  The workaround is to wrap any output in a <div>.
    """
    # allow these tags. Other tags are removed, but their child elements remain
    whitelist = [ 'a', 'abbr', 'acronym', 'address', 'b', 'blockquote', 'br', 'code', 'cite', 'code', 'em', 'i', 'ins', 'kbd', 'p', 'q', 'samp', 'small', 'strike', 'strong', 'sub', 'sup', 'var' ]

    # allow only these attributes on these tags. No other tags are allowed any attributes.
    attr_whitelist = { 'a': ['href', 'title', 'hreflang'], 'img': ['src', 'width', 'height', 'alt', 'title'] }

    # remove these tags, complete with contents.
    blacklist = [ 'script', 'style' ]

    attributes_with_urls = [ 'href', 'src' ]

    # BeautifulSoup is catching out-of-order and unclosed tags, so markup
    # can't leak out of comments and break the rest of the page.
    # TODO: If double-encoding problems arise, convert entities to Unicode.
    # http://www.crummy.com/software/BeautifulSoup/documentation.html#Entity%20Conversion
    soup = BeautifulSoup(untrusted_html)

    # now strip HTML we don't like.
    for tag in soup.findAll():
        if tag.name.lower() in blacklist:
            # blacklisted tags are removed in their entirety
            tag.extract()
        elif tag.name.lower() in whitelist:
            # tag is allowed. Make sure all the attributes are allowed.
            for attr in tag.attrs:
                # allowed attributes are whitelisted per-tag
                if tag.name.lower() in attr_whitelist and attr[0].lower() in attr_whitelist[ tag.name.lower() ]:
                    # some attributes contain urls..
                    if attr[0].lower() in attributes_with_urls:
                        # ..make sure they're nice urls
                        if not re.match(r'(https?|ftp)://', attr[1].lower()):
                            tag.attrs.remove( attr )

                    # ok, then
                    pass
                else:
                    # not a whitelisted attribute. Remove it.
                    tag.attrs.remove( attr )
        else:
            # not a whitelisted tag. I'd like to remove it from the tree
            # and replace it with its children. But that's hard. It's much
            # easier to just replace it with an empty span tag.
            tag.name = "span"
            tag.attrs = []

    # stringify back again
    safe_html = unicode(soup)

    # HTML comments can contain executable scripts, depending on the browser,  
    # so we'll be paranoid and just get rid of all of them  
    # e.g. <!--[if lt IE 7]><script type="text/javascript">h4x0r();</script><![endif]-->  
    # TODO: I rather suspect that this is the weakest part of the operation..
    safe_html = re.sub(r'<!--[.\n]*?-->', '', safe_html)
    
    return safe_html

def strip(untrusted_html):
    """Strips out all tags from untrusted_html, leaving only text.
    Converts XML entities to Unicode characters."""
    soup = BeautifulStoneSoup(untrusted_html, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
    safe_html = ''.join(soup.findAll(text=True))
    return safe_html
        
def main():
    snippet = """<h1>h1 tags are <span style="font-size: 50px;">not allowed</span></h1>
    <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.<br /> Aenean tortor diam, tempor quis, condimentum at, <a href="http://safeurl.com/">sodales</a> non, magna. Duis laoreet nulla non mi. Sed scelerisque nunc a mauris. Fusce pharetra. Aenean sodales augue id ligula.</p>
    <hr>
    <p>Aenean at ante in <a href="javascript:alert('yo');">odio mollis</a> consequat.<br> Cras id risus. Cras facilisis congue orci. Vestibulum eleifend, quam imperdiet ultrices tincidunt, justo leo porta ligula, faucibus aliquet ante <b>quam et odio</b>. Donec eros est, placerat a, eleifend ac, <span style="font-family: 'Comic Sans';">luctus ac</span>, velit. Proin vel dui in erat volutpat porttitor. Suspendisse potenti.</p>
    <blockquote><p>I&#8217;ve seen Plato&apos;s cups &amp; tables, but not his <i>cupness</i> &amp; <i>tableness</i>.</p></blockquote>"""
    
    print "SANITIZED: %s" % sanitize(snippet)
    print "STRIPPED: %s" % strip(snippet)

if __name__ == '__main__':
    main()

