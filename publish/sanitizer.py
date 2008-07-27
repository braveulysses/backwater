#!/usr/bin/env python
# encoding: utf-8
"""
sanitizer.py

Created by Jacob C. on 2008-07-04.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

# TODO: The sanitizer absolutely needs unit tests.

import re
from BeautifulSoup import Comment
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from xml.sax.saxutils import escape

def fix_amp_encoding(txt):
    """Fixes the double encoding that can occur when a string containing named or 
    numeric entities are passed through a typical entity escaping function."""
    fixamps = re.compile('&amp;((#\w+;)|(amp;)|(lt;)|(gt;)|(apos;)|(nbsp;)|(ldquo;)|(rdquo;)|(lsquo;)|(rsquo;)|(quot;)|(middot;))')
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
  
def sanitize(untrusted_html, additional_tags=None):
    """Strips potentially harmful tags and attributes from HTML.
    
    Passing the list additional_tags will add the specified tags to the whitelist.
    
    Based on the work of:
     - Tom Insam <http://jerakeen.org/blog/2008/05/sanitizing-comments-with-python/>
     - akaihola <http://www.djangosnippets.org/snippets/169/>
    """
    # Allow these tags. This can be changed to whatever you please, of course, 
    # either by changing the list in code or by passing alt_whitelist.
    tag_whitelist = [ 
        'a', 'abbr', 'address', 'b', 'blockquote', 
        'br', 'code', 'cite', 'code', 'em', 'i', 'ins', 'kbd', 
        'p', 'q', 'samp', 'small', 'strike', 'strong', 'sub', 
        'sup', 'var' 
    ]
    
    if additional_tags is not None:
        tag_whitelist.extend(additional_tags)
    
    # Allow only these attributes on these tags. No other tags are allowed 
    # any attributes.
    attr_whitelist = { 
        'a': ['href', 'title', 'hreflang'], 
        'img': ['src', 'width', 'height', 'alt', 'title'] 
    }
    
    # Remove these tags, complete with contents.
    tag_blacklist = [ 'script', 'style' ]
    
    attributes_with_urls = [ 'href', 'src' ]
    
    soup = BeautifulSoup(untrusted_html)
    # Remove HTML comments
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
    # Remove unwanted tags
    for tag in soup.findAll():
        # Remove blacklisted tags and their contents.
        if tag.name.lower() in tag_blacklist:
            tag.extract()
        # Hide non-whitelisted tags.
        elif tag.name.lower() not in tag_whitelist:
            tag.hidden = True
        else:
            for attr in tag.attrs:
                # Attributes in the attr_whitelist are considered, but on 
                # a per-tag basis.
                if tag.name.lower() in attr_whitelist and attr[0].lower() in attr_whitelist[ tag.name.lower() ]:
                    # Some attributes contain urls..
                    if attr[0].lower() in attributes_with_urls:
                        # .. so make sure they're nice urls
                        if not re.match(r'(https?|ftp)://', attr[1].lower()):
                            tag.attrs.remove(attr)  
                else:
                    # Non-whitelisted attributes are removed entirely.
                    tag.attrs.remove(attr)
    return unicode(soup)

def strip(untrusted_html):
    """Strips out all tags from untrusted_html, leaving only text.
    Converts XML entities to Unicode characters."""
    soup = BeautifulStoneSoup(untrusted_html, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
    safe_html = ''.join(soup.findAll(text=True))
    return safe_html
        
def main():
    # This is a shitty substitute for a unit test suite.
    snippet = """<h1>h1 tags are not allowed, nor are <span style="font-size: 50px;">style attributes</span></h1>
    <h2>h2 tags aren't allowed, but <b>bold</b> tags are</h2>
    <script type="text/javascript">alert("Script tags are out of the question");</script>
    <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.<br /> Aenean tortor diam, tempor quis, condimentum at, <a href="http://safeurl.com/">totally safe link</a> non, magna. Duis laoreet nulla non mi. Sed scelerisque nunc a mauris. Fusce pharetra. Aenean sodales augue id ligula. An hr follows.</p>
    <hr>
    <p>Aenean at ante in <a href="javascript:alert('yo');">Javascript link</a> consequat.<br> Cras id risus. Cras facilisis congue orci. Vestibulum eleifend, quam imperdiet ultrices tincidunt, justo leo porta ligula, faucibus aliquet ante <b>quam et odio</b>. Donec eros est, placerat a, eleifend ac, <span style="font-family: 'Comic Sans';">luctus ac</span>, velit. Proin vel dui in erat volutpat porttitor. Suspendisse potenti.</p>
    <blockquote><p>I&#8217;ve seen Plato&apos;s cups &amp; tables, but not his <i>cupness</i> &amp; <i>tableness</i>.</p></blockquote>"""
    
    print "SANITIZED: %s" % sanitize(snippet)
    print "***************************************"
    print "STRIPPED: %s" % strip(snippet)

if __name__ == '__main__':
    main()

