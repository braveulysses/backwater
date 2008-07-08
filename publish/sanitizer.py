#!/usr/bin/env python
# encoding: utf-8
"""
sanitizer.py

Created by Jacob C. on 2008-07-04.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import html5lib
import html5lib.sanitizer
import html5lib.treebuilders
try:
    import cElementTree as ElementTree
except:
    import ElementTree as ElementTree

class BackwaterSanitizerMixin(html5lib.sanitizer.HTMLSanitizerMixin):
    acceptable_elements = [ 'a', 'abbr', 'acronym', 'address', 'b', 'big', 'code', 'br', 'cite', 'code', 'em', 'i', 'ins', 'kbd', 'q', 'samp', 'small', 'strike', 'strong', 'sub', 'sup', 'tt', 'u', 'var' ]
    acceptable_protocols = [ 'http', 'https' ]
    
    allowed_elements = acceptable_elements
    # allowed_attributes = acceptable_attributes + mathml_attributes + svg_attributes
    # allowed_css_properties = acceptable_css_properties
    # allowed_css_keywords = acceptable_css_keywords
    # allowed_svg_properties = acceptable_svg_properties
    allowed_protocols = acceptable_protocols

class BackwaterSanitizer(html5lib.tokenizer.HTMLTokenizer, BackwaterSanitizerMixin):
    def __init__(self, stream, encoding=None, parseMeta=True, useChardet=True,
                 lowercaseElementName=False, lowercaseAttrName=False):
        super(BackwaterSanitizer, self).__init__(stream, encoding, parseMeta, useChardet, lowercaseElementName, lowercaseAttrName)
        
def main():
    snippet = """<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean tortor diam, tempor quis, condimentum at, sodales non, magna. Duis laoreet nulla non mi. Sed scelerisque nunc a mauris. Fusce pharetra. Aenean sodales augue id ligula. Aenean at ante in <a href="javascript:alert('yo');">odio mollis</a> consequat. Cras id risus. Cras facilisis congue orci. Vestibulum eleifend, quam imperdiet ultrices tincidunt, justo leo porta ligula, faucibus aliquet ante <b>quam et odio</b>. Donec eros est, placerat a, eleifend ac, <span style="font-family: 'Comic Sans';">luctus ac</span>, velit. Proin vel dui in erat volutpat porttitor. Suspendisse potenti.</p>"""
    
    parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("beautifulsoup"), tokenizer=BackwaterSanitizer)
    output = parser.parse(snippet)
    print output

if __name__ == '__main__':
    main()

