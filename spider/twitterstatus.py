#!/usr/bin/env python
# encoding: utf-8
"""
twitterstatus.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

from httplib import BadStatusLine
from urllib2 import HTTPError
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

    def get_tweet_url(self, id):
        return 'http://twitter.com/' + self.name + '/tweets/' + str(id)

    def parse(self):
        """Fetches Twitter tweets using the Twitter API."""
        self.logger.debug("Contacting Twitter services")
        try:
            twitty = twitter.Api(
                username=config.TWITTER_ACCOUNT, 
                password=config.TWITTER_PASSWORD
            )
            self.logger.info("Getting Twitter tweets for %s" % self.owner)
            tweets = twitty.GetUserTimeline(self.name)
            for tweet in tweets:
                e = Quote()
                e.source_name = self.name
                e.source_url = self.url
                e.author = tweet.user.name
                e.summary = tweet.text
                e.content = e.summary
                e.citation = e.author
                self.logger.info("Twitter: '%s'" % e.summary)
                e.url = self.get_tweet_url(tweet.id)
                self.logger.debug("Twitter URL: %s" % e.url)
                e.date = tweet.created_at
                self.entries.append(e)
        except BadStatusLine:
            self.logger.exception("Twitter.com unexpectedly closed the connection!")
        except HTTPError, err:
            self.logger.exception("HTTP error: '%s'" % err)
        except:
            self.logger.exception("Unknown error while fetching Twitter tweet!")

def main():
    pass

if __name__ == '__main__':
    main()

