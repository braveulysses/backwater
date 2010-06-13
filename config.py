#!/usr/bin/env python
# # -*- coding: utf-8 -*-
"""
config.py

Created by Jacob C. on 2008-06-26.
Copyright (c) 2010 Spaceship No Future. All rights reserved.
"""

__version__ = '0.9.1'
__author__ = "SNF Labs <jacob@spaceshipnofuture.org>"

import os
import logging

#### Bot attributes ####
BOT_NAME = 'chompybot'
BOT_URL = 'http://labs.spaceshipnofuture.org/backwater/'
BOT_USER_AGENT = BOT_NAME + '/' + __version__ + ' +' + BOT_URL

#### Data directories ####
DATA_DIR = os.getcwd() + os.sep + 'data'
TEMPLATE_DIR = os.getcwd() + os.sep + 'templates'
CACHE_DIR = DATA_DIR + os.sep + 'cache'
OUTPUT_DIR = DATA_DIR + os.sep + 'output'
LOG_DIR = DATA_DIR + os.sep + 'logs'
IMAGE_CACHE_DIR = OUTPUT_DIR + os.sep + 'images'
SOURCES_CACHE_FILE = CACHE_DIR + os.sep + '_sources.cache'
ENTRIES_CACHE_FILE = CACHE_DIR + os.sep + '_entries.cache'

#### Templates ####
HTML5_TEMPLATE = TEMPLATE_DIR + os.sep + 'chompy.html5.mako'
ATOM_TEMPLATE = TEMPLATE_DIR + os.sep + 'chompy.atom.mako'

#### Output ####
NUM_ENTRIES = 75
HTML5_OUTPUT_FILE = OUTPUT_DIR + os.sep + 'chompy.html'
ATOM_OUTPUT_FILE = OUTPUT_DIR + os.sep + 'chompy.atom'
ATOM_LINKS_OUTPUT_FILE = OUTPUT_DIR + os.sep + 'links.atom'

BASE_URL = 'http://chompy.net'
FEEDS_URL = '/feeds'
IMAGES_URL = '/images/backwater'

ATOM_FEED_TITLE = 'chompy.net'
ATOM_FEED_SUBTITLE = 'more rocks and garbage'
ATOM_FEED_URL = 'http://chompy.net/feeds/chompy.atom'

ATOM_LINKS_FEED_TITLE = 'chompy.net: links'
ATOM_LINKS_FEED_SUBTITLE = 'the SNF link blogs'
ATOM_LINKS_FEED_URL = 'http://chompy.net/feeds/links.atom'

#### Pickle options ####
CACHE_THRESHOLD = 15 # minutes

#### Caching options ####
HTTP_CHECK_CACHE = True
ENTRIES_CHECK_CACHE = True

#### Logging ####
DEFAULT_LOG_NAME = 'backwater.log'
ERROR_LOG_NAME = 'error.log'
LOG_FORMAT = "%(asctime)s: %(name)s: %(levelname)s: %(message)s"
DEFAULT_LOG_LEVEL = logging.DEBUG
ERROR_LOG_LEVEL = logging.ERROR
CH_LOG_LEVEL = logging.ERROR
MAX_LOG_SIZE = 1024 * 192
MAX_LOGS = 5

#### Text processing options ####
WORD_LIMIT = 150

#### Time formats ####
ATOM_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
HTML_TIME_FORMAT = "%A, %B %d"

#### Source-level options ####
TWITTER_IGNORE_REPLIES = True
TWITTER_IGNORE_RETWEETS = True

#######################################################################
#
# STOP EDITING HERE
#
#######################################################################

#### Keys, API accounts ####
FLICKR_KEY = os.getenv("BACKWATER_FLICKR_KEY")
TWITTER_ACCOUNT = os.getenv("BACKWATER_TWITTER_ACCOUNT")
TWITTER_PASSWORD = os.getenv("BACKWATER_TWITTER_PASSWORD")

class ConfigurationError(Exception): pass

def check_environment():
    sensitive_configs = [
        FLICKR_KEY,
        TWITTER_ACCOUNT,
        TWITTER_PASSWORD
    ]
    for config in sensitive_configs:
        if config is None or config == "":
            raise ConfigurationError
