#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
backwater.py

Created by Jacob C. on 2008-02-19.
Copyright (c) 2010 SNF Labs. All rights reserved.
"""

import os
import sys
import getopt
import yaml
import logging
import logging.handlers
import config
import setup
import spider
import publish

from vlassic import BackwaterCache

# Sources (feeds) and subtypes of sources

from spider.source import Source
from spider.weblog import Weblog
from spider.linklog import Linklog
from spider.commentlog import Commentlog
from spider.tumblelog import Tumblelog
from spider.photostream import Photostream
from spider.twitterstatus import TwitterStatus

# Entries and subtypes of entries.

# from entries import Entry
# from entries import Post
# from entries import Link
# from entries import Quote
# from entries import Conversation
# from entries import Song
# from entries import Video
# from entries import Photo

# HTTP exceptions

from spider import BackwaterHTTPError
from spider import InternalServerError
from spider import BadGatewayError
from spider import ServiceUnavailableError
from spider import BadRequestError
from spider import NotAuthorizedError
from spider import URLNotFoundError
from spider import URLForbiddenError
from spider import URLGoneError
from spider import UnsupportedContentTypeError

# Other exceptions

from config import ConfigurationError

#############################################################################

from config import __version__
from config import __author__

version_message = '''Backwater v%s
2008, %s''' % (__version__, __author__)

# Keep this in sync with the call to getopt.getopt() down in main()
help_message = """Usage: python %s
Update the chompy.net aggregator.

    -h, --help              show this help message
    -V, --version           show version number
    -s, --sources=FILE      specify alternate sources file 
                            (default is 'sources.yaml')
        --no-http-cache     ignore the HTTP cache
        --no-entries-cache  ignore the entries cache
    -f  --flush             flush all caches
    -r, --rebuild           rebuild output files without updating feeds
    -l, --list              list all sources
""" % sys.argv[0]

#############################################################################

# Check for and create data directories
setup.create_data_directories()

# Set up logging
logger = logging.getLogger("backwater")
logger.setLevel(logging.DEBUG)

# Default file handler
default_fn = config.LOG_DIR + os.sep + config.DEFAULT_LOG_NAME
if os.path.exists(config.LOG_DIR):
    default_fh = logging.handlers.RotatingFileHandler(default_fn, 'a', config.MAX_LOG_SIZE, config.MAX_LOGS)
else:
    # TODO: Don't raise a string exception, make a class
    raise "Log directory does not exist: '%s'" % config.LOG_DIR
default_fh.setLevel(config.DEFAULT_LOG_LEVEL)

# Error file handler
# error_fn = config.LOG_DIR + os.sep + config.ERROR_LOG_NAME
# if os.path.exists(config.LOG_DIR):
#     error_fh = logging.handlers.RotatingFileHandler(error_fn, 'a', config.MAX_LOG_SIZE, config.MAX_LOGS)
# else:
#     raise "Log directory does not exist: '%s'" % config.LOG_DIR
# error_fh.setLevel(config.DEFAULT_LOG_LEVEL)

# Console handler
ch = logging.StreamHandler(sys.stderr)
ch.setLevel(config.CH_LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)
default_fh.setFormatter(formatter)
# error_fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(default_fh)
# logger.addHandler(error_fh)
logger.addHandler(ch)

#############################################################################

class UnknownSourceTypeError(Exception): pass
class CacheNotFoundError(Exception): pass

def get_sources(sources_file):
    """Retrieves and parses the sources.yaml file for source information."""
    sources = []
    try:
        logger.debug("Opening '%s'" % sources_file)
        f = open(sources_file, 'r')
        logger.debug("Loading YAML")
        y = yaml.load(f)
        f.close()
        for src in y['sources']:
            s = None
            # Deal with special cases
            try:
                excluded_types = src['excluded_types']
            except KeyError:
                excluded_types = []
            try:
                excluded_keywords = src['excluded_keywords']
            except KeyError:
                excluded_keywords = []
            # Instantiate each source
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
                        src['url'], 
                        excluded_types
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
                        src['url'],
                        excluded_keywords
                    )
                else:
                    raise UnknownSourceTypeError
                sources.append(s)
            except KeyError:
                logger.error("Problem parsing: %s" % src)
            except UnknownSourceTypeError:
                logger.error("Unknown source type encountered: %s" % src)
        return sources
    except IOError:
        logger.critical("Couldn't load the sources file '%s'!" % sources_file)
        raise

def write_output(entries):
    # Write HTML output
    logger.debug("Publishing HTML 5 file...")
    publish.publish(
        config.HTML5_TEMPLATE, 
        config.HTML5_OUTPUT_FILE, 
        entries[:config.NUM_ENTRIES]
    )
    # Write Atom output
    logger.debug("Publishing Atom file...")
    publish.publish(
        config.ATOM_TEMPLATE, 
        config.ATOM_OUTPUT_FILE, 
        entries[:config.NUM_ENTRIES], 
        opt_template_values = {
            'feed_title': config.ATOM_FEED_TITLE, 
            'feed_subtitle': config.ATOM_FEED_SUBTITLE, 
            'feed_url': config.ATOM_FEED_URL
        }
    )
    # Write a link-only feed
    links = []
    for entry in entries:
        if entry.type == 'link':
            links.append(entry)
    logger.debug("Publishing Atom links file...")
    publish.publish(
        config.ATOM_TEMPLATE,
        config.ATOM_LINKS_OUTPUT_FILE,
        links[:config.NUM_ENTRIES], 
        opt_template_values = {
            'feed_title': config.ATOM_LINKS_FEED_TITLE, 
            'feed_subtitle': config.ATOM_LINKS_FEED_SUBTITLE, 
            'feed_url': config.ATOM_LINKS_FEED_URL
        }
    )

class FlushCache(Exception):
    """Flushes the content cache."""
    pass    

class Version(Exception):
    """Outputs version information."""
    def __init__(self, msg):
        self.msg = msg

class Usage(Exception):
    """Outputs a command-line usage message."""
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    # If this is true, enables normal processing.
    # Otherwise, all that is skipped.
    do_update = True
    # If this is true, forces backwater to use the pickled entries 
    # to rebuild output.  Skips HTTP fetching.
    # Otherwise, normal processing occurs.
    force_rebuild = False
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(
                argv[1:], 
                "Vhs:frl", 
                [ "version", 
                  "help", 
                  "sources=", 
                  "no-http-cache",
                  "no-entries-cache",
                  "flush", 
                  "rebuild", 
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
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-s", "--sources"):
                logger.debug("Using sources file: '%s'" % value)
                sources_file = value
            if option in ("--no-http-cache"):
                config.HTTP_CHECK_CACHE = False
            if option in ("--no-entries-cache"):
                config.ENTRIES_CHECK_CACHE = False
            if option in ("-f", "--flush"):
                raise FlushCache()
            if option in ("-r", "--rebuild"):
                print "Skipping HTTP fetching, rebuilding output..."
                force_rebuild = True
            if option in ("-l", "--list"):
                do_update = False
    
        # Okay, GO
        # Parse sources.yaml and instantiate sources
        try:
            if do_update:
                # First, make sure the environment is initialized
                config.check_environment()
                
                entries = []
                entries_cache = BackwaterCache(config.ENTRIES_CACHE_FILE)
                if (force_rebuild or entries_cache.is_fresh(config.CACHE_THRESHOLD)) and \
                    (config.ENTRIES_CHECK_CACHE == True):
                    logger.info("Using cached entries...")
                    try:
                        entries = entries_cache.restore()
                    except IOError:
                        raise CacheNotFoundError()
                else:
                    logger.debug("Reading sources from '%s'" % sources_file)
                    sources = get_sources(sources_file)
                    # Update sources
                    if config.ENTRIES_CHECK_CACHE:
                        logger.debug("Entries cache is stale...")
                    else:
                        logger.debug("Skipping entries cache...")
                    logger.debug("Starting parsing run")
                    entries = spider.update(sources)
                    # Sort
                    entries.sort()
                    entries.reverse()
                    logger.debug("Caching entries...")
                    # The pickler can't save anything with logger objects 
                    # because of thread locks (?), so zap them
                    for entry in entries:
                        entry.logger = None
                    entries_cache.save(entries)
                write_output(entries)
                logger.info("Finished processing.")
            else:
                # List sources but don't do anything else
                logger.debug("Reading sources from '%s'" % sources_file)
                sources = get_sources(sources_file)
                logger.debug("Listing sources; no parsing")
                for src in sources:
                    print src
        except ConfigurationError:
            print >> sys.stderr, "ERROR: Complete configuration data not found!"
            print >> sys.stderr, "Be sure to define all of the following environment variables:"
            print >> sys.stderr
            print >> sys.stderr, "    BACKWATER_FLICKR_KEY"
            print >> sys.stderr, "    BACKWATER_TWITTER_ACCOUNT"
            print >> sys.stderr, "    BACKWATER_TWITTER_PASSWORD"
            print >> sys.stderr
            return 1
        except CacheNotFoundError:
            print >> sys.stderr, "ERROR: Entries cache not found!"
            return 1
        except yaml.parser.ParserError, e:
            print >> sys.stderr, "ERROR: Couldn't parse sources file: %s" % e
            return 1
        except IOError:
            return 1
        except:
            logger.exception("Unknown exception encountered")
            raise

    except FlushCache:
        # TODO: Implement "flush" command to clear HTTP and entries cache
        print "Flushing the cache is currently unimplemented."
        print "To manually flush the cache delete the contents of "
        print "the directory %s." % (config.CACHE_DIR)
        print
        return 0

    except Version, err:
        print str(err.msg)
        return 2
    
    except Usage, err:
        print str(err.msg)
        return 2
    
    except KeyboardInterrupt:
        print >> sys.stderr, "Manually terminated."
        return 3


if __name__ == "__main__":
    sys.exit(main())
