#!/usr/bin/env python
# encoding: utf-8
"""
backwater.py

Created by Jacob C. on 2008-02-19.
Copyright (c) 2008 SNF Labs. All rights reserved.
"""

import sys
import getopt
import yaml
import config

# Sources (feeds) and subtypes of sources

from spider.source import Source
from spider.weblog import Weblog
from spider.linklog import Linklog
from spider.commentlog import Commentlog
from spider.tumblelog import Tumblelog
from spider.photostream import Photostream
from spider.twitterstatus import TwitterStatus

# Entries and subtypes of entries.

from entries import Entry
from entries import Post
from entries import Link
from entries import Quote
from entries import Conversation
from entries import Song
from entries import Video
from entries import Photo

#############################################################################

from config import __version__
from config import __author__

version_message = '''Backwater v%s
2008, %s''' % (__version__, __author__)

help_message = """Usage: python %s
Update the chompy.net aggregator.

    -h, --help              show this help message
    -V, --version           show version number
    -v, --verbose           execute with verbose output
    -s, --sources=FILE      specify alternate sources file 
                            (default is 'sources.yaml')
    -f, --flush             flush the cache
    -l, --list              list all sources
""" % sys.argv[0]

#############################################################################

class UnknownSourceTypeError(Exception): pass

def get_sources(sources_file):
    """Retrieves and parses the sources.yaml file for source information."""
    sources = []
    try:
        f = open(sources_file, 'r')
        y = yaml.load(f)
        f.close()
        for src in y['sources']:
            s = None
            try:
                if src['type'] == 'weblog':
                    s = Weblog(
                        src['name'], 
                        src['owner'], 
                        src['url'], 
                        src['feed_url']
                    )
                elif src['type'] == 'linklog':
                    s = Linklog(
                        src['name'], 
                        src['owner'], 
                        src['url'], 
                        src['feed_url']
                    )
                elif src['type'] == 'commentlog':
                    s = Commentlog(
                        src['name'], 
                        src['owner'], 
                        src['url'], 
                        src['feed_url']
                    )
                elif src['type'] == 'tumblelog':
                    s = Tumblelog(
                        src['name'], 
                        src['owner'], 
                        src['url']
                    )
                elif src['type'] == 'photostream':
                    s = Photostream(
                        src['name'], 
                        src['owner'], 
                        src['url'], 
                        src['flickr_id']
                    )
                elif src['type'] == 'twitter':
                    s = TwitterStatus(
                        src['name'], 
                        src['owner'], 
                        src['url']
                    )
                else:
                    raise UnknownSourceTypeError
                sources.append(s)
            except KeyError:
                print "Problem parsing: %s" % (src)
            except UnknownSourceTypeError:
                print "Unknown source type encountered: %s" % (src)
        return sources
    except IOError:
        print >> sys.stderr, "Couldn't load the config file %s!" % (config_file)
        raise

class Version(Exception):
    """Outputs version information."""
    def __init__(self, msg):
        self.msg = msg

class Usage(Exception):
    """Outputs a command-line usage message."""
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    update = True
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(
                argv[1:], 
                "Vho:vs:fl", 
                [ "version", 
                  "verbose", 
                  "help", 
                  "output=", 
                  "sources=", 
                  "flush", 
                  "list" ]
            )
        except getopt.error, msg:
            raise Usage(msg)
        
        # Default sources file
        sources_file = 'sources.yaml'
    
        # Option processing
        for option, value in opts:
            if option in ("-V", "--version"):
                raise Version(version_message)
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option in ("-s", "--sources"):
                config_file = value
            if option in ("-f", "--flush"):
                pass
            if option in ("-l", "--list"):
                update = False
    
        # Okay, GO
        # Parse sources.yaml and instantiate sources
        try:
            sources = get_sources(sources_file)
            if update:
                # Update sources
                for src in sources:
                    # Spider and parse sources
                    print src.name
                    src.parse()
                    # Merge, sort, and collate
                    # Write output
            else:
                # List sources but don't do anything else
                for src in sources:
                    print src
        except IOError:
            return 1
        except:
            raise
    
    except Version, err:
        print >> sys.stderr, str(err.msg)
        return 2
    
    except Usage, err:
        print >> sys.stderr, str(err.msg)
        return 2


if __name__ == "__main__":
    sys.exit(main())
