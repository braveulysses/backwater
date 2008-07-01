#!/usr/bin/env python
# encoding: utf-8
"""
twitterstatus.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import urllib2
import httplib
import twitter
import logging
import config
from source import Source
from entries import Quote

module_logger = logging.getLogger("backwater.twitterstatus")

class TwitterStatus(Source):
    def __init__(self, name, owner, url):
        super(TwitterStatus, self).__init__(name, owner, url)
        self.logger = logging.getLogger("backwater.twitterstatus.TwitterStatus")
        self.type = 'twitterstatus'
        self.entry_type = 'quote'

    def get_status_url(self, id):
        return 'http://twitter.com/' + self.name + '/statuses/' + str(id)

    def parse(self):
        """Fetches Twitter status using the Twitter API."""
        self.logger.debug("Contacting Twitter services")
        try:
            twitty = twitter.Api(
                username=config.TWITTER_ACCOUNT, 
                password=config.TWITTER_PASSWORD
            )
            self.logger.info("Getting Twitter statuses for %s" % self.owner)
            statuses = twitty.GetUserTimeline(self.name)
            for status in statuses:
                self.author = status.user.name
                self.summary = status.text
                self.content = self.summary
                self.logger.info("Twitter: '%s'" % self.summary)
                self.url = self.get_status_url(status.id)
                self.logger.debug("Twitter URL: %s" % self.url)
                self.date = status.created_at
        except httplib.BadStatusLine:
            self.logger.exception("Twitter.com unexpectedly closed the connection!")
        except urllib2.HTTPError, err:
            self.logger.exception("HTTP error: '%s'" % err)
        except:
            self.logger.exception("Unknown error while fetching Twitter status!")

def main():
    pass

if __name__ == '__main__':
    main()

