#!/usr/bin/env python
# encoding: utf-8
"""
vlassic.py

Backwater pickling routines. Not to be confused with the HTTP caching 
performed by httplib2.

Created by Jacob C. on 2008-07-27.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import os
import pickle
from datetime import datetime
from datetime import timedelta
import logging
import config

module_logger = logging.getLogger("backwater.vlassic")

class BackwaterCacheError(Exception): pass

class BackwaterCache(object):
    """The Backwater data cache, a wrapper around the pickle module."""
    def __init__(self, cache_file):
        super(BackwaterCache, self).__init__()
        self.cache_file = cache_file
        self.PICKLE_PROTOCOL = 2

    def is_fresh(self, minutes):
        """Is the pickle fresh or stale? 
        Takes the value minutes, which is the cache threshold.
        
        Returns true if the pickle file is fresh, 
        false if it is stale or nonexistent.
        """
        try:
            stat_info = os.stat(self.cache_file)
            mtime = datetime.fromtimestamp(stat_info.st_mtime)
            current_time = datetime.now()
            threshold = timedelta(minutes=minutes)
            return threshold > (current_time - mtime)
        except OSError:
            return False

    def save(self, obj):
        f = open(self.cache_file, 'wb')
        pickle.dump(obj, f, self.PICKLE_PROTOCOL)
        f.close()
        
    def restore(self):
        f = open(self.cache_file, 'rb')
        obj = pickle.load(f)
        f.close()
        return obj

def main():
    pass

if __name__ == '__main__':
    main()

