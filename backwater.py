#!/usr/bin/env python
# encoding: utf-8
"""
backwater.py

Created by Jacob C. on 2008-02-19.
Copyright (c) 2008 SNF Labs. All rights reserved.
"""

__version__ = '0.1'
__author__ = "SNF Labs <jacob@spaceshipnofuture.org>"

import sys
import getopt
import yaml

version_message = '''Backwater v%s
2008, %s''' % (__version__, __author__)

help_message = '''
The help message goes here.
'''

#############################################################################

# Sources (feeds) and subtypes of sources.

class Source: pass

class Weblog(Source): pass

class Linklog(Source): pass

class Tumblelog(Source): pass

class Photostream(Source): pass

class TwitterStatus(Source): pass

# Entries and subtypes of entries.

class Entry: pass

class Post(Entry): pass

class Link(Entry): pass

class Quote(Entry): pass

class Song(Entry): pass

class Video(Entry): pass

class Photo(Entry): pass

#############################################################################

def get_configuration(config_file):
    try:
        f = open(config_file, 'r')
        config = yaml.load(f)
        f.close()
        return config
    except IOError:
        print >> sys.stderr, "Couldn't load the config file %s!" % (config_file)
        raise

class Version(Exception):
    def __init__(self, msg):
        self.msg = msg

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "Vho:vc:", ["version", "help", "output=", "config="])
        except getopt.error, msg:
            raise Usage(msg)
        
        # Default config file
        config_file = 'config.yaml'
    
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
            if option in ("-c", "--config"):
                config_file = value
    
        # Okay, GO
        # Read configuration
        try:
            config = get_configuration(config_file)
            print yaml.dump(config)
        except IOError:
            return 1
        except:
            raise
        # Get feeds
        # Get tumblelogs
        # Get twitters
        # Get photos
        # Merge, sort, and collate
        # Write output
    
    except Version, err:
        print >> sys.stderr, str(err.msg)
        return 2
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
