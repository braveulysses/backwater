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

help_message = '''
The help message goes here.
'''

#################################################

# Sources (feeds) and subtypes of sources.

class Source: pass

class Weblog(Source): pass

class Linklog(Source): pass

class Tumblelog(Source): pass

class Photostream(Source): pass

class Twitter(Source): pass

# Entries and subtypes of entries.

class Entry: pass

class Post(Entry): pass

class Link(Entry): pass

class Quote(Entry): pass

class Song(Entry): pass

class Video(Entry): pass

class Photo(Entry): pass

#################################################

def get_configuration(config_file):
    try:
        f = open(config_file, 'r')
        config = yaml.load(f)
        return config
    finally:
        f.close()

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
		except getopt.error, msg:
			raise Usage(msg)
	
		# Option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-o", "--output"):
				output = value
				
		# Okay, GO
		# Read configuration
		config = get_configuration('config.yaml')
		print yaml.dump(config)
		# Get feeds
		# Get tumblelogs
		# Get twitters
		# Get photos
		# Merge, sort, and collate
		# Write output
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	sys.exit(main())
