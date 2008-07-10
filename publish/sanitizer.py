#!/usr/bin/env python
# encoding: utf-8
"""
sanitizer.py

Created by Jacob C. on 2008-07-04.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import re
from BeautifulSoup import BeautifulSoup
# import html5lib
# import html5lib.sanitizer
# import html5lib.treebuilders
# try:
#     import cElementTree as ElementTree
# except:
#     import ElementTree as ElementTree

# class BackwaterSanitizerMixin(html5lib.sanitizer.HTMLSanitizerMixin):
#     acceptable_elements = [ 'a', 'abbr', 'acronym', 'address', 'b', 'big', 'code', 'br', 'cite', 'code', 'em', 'i', 'ins', 'kbd', 'q', 'samp', 'small', 'strike', 'strong', 'sub', 'sup', 'tt', 'u', 'var' ]
#     acceptable_protocols = [ 'http', 'https' ]
#     
#     allowed_elements = acceptable_elements
#     # allowed_attributes = acceptable_attributes + mathml_attributes + svg_attributes
#     # allowed_css_properties = acceptable_css_properties
#     # allowed_css_keywords = acceptable_css_keywords
#     # allowed_svg_properties = acceptable_svg_properties
#     allowed_protocols = acceptable_protocols
# 
# class BackwaterSanitizer(html5lib.tokenizer.HTMLTokenizer, BackwaterSanitizerMixin):
#     def __init__(self, stream, encoding=None, parseMeta=True, useChardet=True,
#                  lowercaseElementName=False, lowercaseAttrName=False):
#         super(BackwaterSanitizer, self).__init__(stream, encoding, parseMeta, useChardet, lowercaseElementName, lowercaseAttrName)
        
def sanitize(evil_html):
    """Strips dangerous tags and attributes from HTML.
    
    Based on the work of Tom Insam:
    http://jerakeen.org/blog/2008/05/sanitizing-comments-with-python/
    """
    # allow these tags. Other tags are removed, but their child elements remain
    whitelist = ['blockquote', 'em', 'i', 'img', 'strong', 'u', 'a', 'b', "p", "br", "code", "pre" ]

    # allow only these attributes on these tags. No other tags are allowed any attributes.
    attr_whitelist = { 'a':['href','title','hreflang'], 'img':['src', 'width', 'height', 'alt', 'title'] }

    # remove these tags, complete with contents.
    blacklist = [ 'script', 'style' ]

    attributes_with_urls = [ 'href', 'src' ]

    # BeautifulSoup is catching out-of-order and unclosed tags, so markup
    # can't leak out of comments and break the rest of the page.
    soup = BeautifulSoup(evil_html)

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
    # TODO - I rather suspect that this is the weakest part of the operation..
    safe_html = re.sub(r'<!--[.\n]*?-->','',safe_html)
    
    return safe_html
        
def main():
    snippet = """<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean tortor diam, tempor quis, condimentum at, sodales non, magna. Duis laoreet nulla non mi. Sed scelerisque nunc a mauris. Fusce pharetra. Aenean sodales augue id ligula.</p><hr><p>Aenean at ante in <a href="javascript:alert('yo');">odio mollis</a> consequat. Cras id risus. Cras facilisis congue orci. Vestibulum eleifend, quam imperdiet ultrices tincidunt, justo leo porta ligula, faucibus aliquet ante <b>quam et odio</b>. Donec eros est, placerat a, eleifend ac, <span style="font-family: 'Comic Sans';">luctus ac</span>, velit. Proin vel dui in erat volutpat porttitor. Suspendisse potenti.</p>"""
    
    # parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("beautifulsoup"), tokenizer=BackwaterSanitizer)
    # output = parser.parse(snippet)
    # print output
    print sanitize(snippet)

if __name__ == '__main__':
    main()

