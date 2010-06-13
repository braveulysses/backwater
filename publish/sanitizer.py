#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sanitizer.py

Created by Jacob C. on 2008-07-04.
Copyright (c) 2010 Spaceship No Future. All rights reserved.
"""

import re
from BeautifulSoup import Tag
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

def heading_to_bold(txt, add_break=False):
    """Replaces heading tags (<h1>, <h2>, etc.) with <b> tags.
    
    Optionally appends two <br>s."""
    soup = BeautifulSoup(txt)
    headers = soup.findAll([ 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for header in headers:
        bold_tag = Tag(soup, "b", [])
        bold_tag.contents = header.contents
        header.replaceWith(bold_tag)
        if add_break:
            header.append(Tag(soup, "br"))
            header.append(Tag(soup, "br"))
    return unicode(soup)

def block_to_break(txt):
    """Removes block-level tags and, where two block tags meet, inserts two <br>s."""
    soup = BeautifulSoup(txt)
    blocks = soup.findAll([ 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'footer', 'nav', 'section', 'article', 'blockquote', 'div', 'p' ])
    counter = 1
    end = len(blocks)
    for block in blocks:
        if end > 1 and counter != end:
            block.append(Tag(soup, "br"))
            block.append(Tag(soup, "br"))
        block.hidden = True
        counter = counter + 1
    return unicode(soup)

def sanitize(untrusted_html, additional_tags=None):
    """Strips potentially harmful tags and attributes from HTML, but preserves 
    all tags in a whitelist.
    
    Passing the list additional_tags will add the specified tags to the whitelist.
    
    The sanitizer does NOT encode reserved characters into XML entities.  It is up 
    to the template code, if any, to take care of that.
    
    Based on the work of:
     - Tom Insam <http://jerakeen.org/blog/2008/05/sanitizing-comments-with-python/>
     - akaihola <http://www.djangosnippets.org/snippets/169/>
    """
    # Allow these tags. This can be changed to whatever you please, of course, 
    # either by changing the list in code or by passing alt_whitelist.
    tag_whitelist = [ 
        'a', 'abbr', 'address', 'b', 'code', 
        'cite', 'code', 'em', 'i', 'ins', 'kbd', 
        'q', 'samp', 'small', 'strike', 'strong', 'sub', 
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

    Converts XML entities to Unicode characters.  This is desirable because it 
    reduces the likelihood that a filter further down the text processing chain 
    will double-encode the XML entities."""
    soup = BeautifulStoneSoup(untrusted_html, convertEntities=BeautifulStoneSoup.ALL_ENTITIES)
    safe_html = ''.join(soup.findAll(text=True))
    return safe_html
        
def main():
    pass

if __name__ == '__main__':
    main()

