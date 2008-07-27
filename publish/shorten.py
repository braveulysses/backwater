#!/usr/bin/env python
# encoding: utf-8
"""
shorten.py

Created by Jacob C. on 2008-07-24.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import logging
module_logger = logging.getLogger("backwater.publish.shorten")

def wc(text):
    try:
        return len(text.split())
    except:
        module_logger.exception("Trouble getting word count for: '%s'" % text)
        raise

def shorten(text, limit):
    try:
        if (wc(text) > limit):
            words = text.split()
            text = ''
            for i in range(limit):
                text = text + ' ' + words[i]
            text = text + '&#8230;'
        return text
    except:
        module_logger.exception("Trouble truncating string: '%s'" % text)
        raise

def main():
    text = "there are five new tomato plants, all in new places; where they were all on the west row last year, now they're all on the south, with one in the west. we also planted new eggplant, salad burnet, flax, basil, and artichoke. the artichoke is on the opposite corner as last year, and the eggplant has moved south. they say you have to plan for succession planting, but when you've got the right friends, it really makes these things far simpler."
    print "The following number should be 81: %s" % (wc(text))
    print "Also: %s" % (shorten(text, 10))

if __name__ == '__main__':
    main()

