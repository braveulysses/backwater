#!/usr/bin/env python
# encoding: utf-8
"""
twitterstatus.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import twitter
import logging
import config
import re
from httplib import BadStatusLine
from urllib2 import HTTPError
from feedparser import _parse_date as parse_date
from source import Source
from entries import Quote

module_logger = logging.getLogger("backwater.twitterstatus")

class TwitterStatus(Source):
    def __init__(self, name, owner, url, excluded_keywords=None):
        super(TwitterStatus, self).__init__(name, owner, url)
        self.logger = logging.getLogger("backwater.twitterstatus.TwitterStatus")
        self.type = 'twitterstatus'
        self.excluded_keywords = excluded_keywords

    def get_tweet_url(self, tweet_id):
        return 'http://twitter.com/' + self.name + '/statuses/' + str(tweet_id)
    
    @classmethod
    def link_users(cls, txt):
        rx = re.compile(r"@(\S+)")
        repl = r"""@<a href="http://twitter.com/\g<1>/">\g<1></a>"""
        return rx.sub(repl, txt)    
    
    @classmethod
    def link_hashtags(cls, txt):
        rx = re.compile(r"#(\S+)")
        repl = r"""<a href="http://twitter.com/search?q=%23\g<1>">#\g<1></a>"""
        return rx.sub(repl, txt)

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
                skip = False
                e = Quote()
                e.source.name = self.name
                e.source.url = self.url
                e.author = tweet.user.name
                e.title = "Tweet from %s" % e.author
                e.summary = tweet.text
                e.content = e.summary
                # Add hyperlinks
                # e.content = TwitterStatus.link_users(e.content)
                # e.content = TwitterStatus.link_hashtags(e.content)
                e.citation = e.author
                self.logger.info("Tweet: '%s'" % e.summary)
                e.url = self.get_tweet_url(tweet.id)
                self.logger.debug("Tweet URL: %s" % e.url)
                e.date = tweet.created_at
                e.date_parsed = parse_date(e.date)
                self.logger.debug("Tweet date: %s" % e.date_as_string(e.date_parsed))
                # Skip this tweet if it's in the exclusion list
                if self.excluded_keywords is not None:
                    for keyword in self.excluded_keywords:
                        self.logger.debug("Checking for excluded keyword: '%s'" % keyword)
                        if e.summary.lower().find(keyword.lower()) > -1:
                            self.logger.debug("Skipping tweet with excluded keyword: '%s'" % keyword)
                            skip = True
                if skip:
                    continue
                else:
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

