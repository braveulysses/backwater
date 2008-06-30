#!/usr/bin/env python
# encoding: utf-8
"""
source.py

Created by Jacob C. on 2008-06-22.
Copyright (c) 2008 Spaceship No Future. All rights reserved.
"""

import httplib2
import logging
import config

module_logger = logging.getLogger("backwater.source")

def source_string(name, type, owner, url):
    return """%s
  Type: %s
  Owner: %s
  URL: %s""" % (name, type, owner, url)

class BackwaterHTTPError(Exception): pass
class InternalServerError(BackwaterHTTPError): pass
class BadGatewayError(BackwaterHTTPError): pass
class ServiceUnavailableError(BackwaterHTTPError): pass
class BadRequestError(BackwaterHTTPError): pass
class NotAuthorizedError(BackwaterHTTPError): pass
class URLNotFoundError(BackwaterHTTPError): pass
class URLForbiddenError(BackwaterHTTPError): pass
class URLGoneError(BackwaterHTTPError): pass

class UnsupportedContentTypeError(BackwaterHTTPError):
    def __init__(self, msg):
        self.msg = msg
    
class BadContentTypeError(BackwaterHTTPError): pass

class Source(object):
    def __init__(self, name, owner, url):
        super(Source, self).__init__()
        self.logger = logging.getLogger("backwater.source.Source")
        self.type = 'source'
        self.entry_type = None
        self.name = name
        self.owner = owner
        self.url = url
        self.entries = []
        self.http_content = None
        self.http_response = None

    def __str__(self):
        return source_string(self.name, self.type, self.owner, self.url)

    def _parse_content_type(self, ct):
        """Given an HTTP content-type header, parses out the content-type and 
        the charset.

        Does not currently perform any validation on the content of the header."""
        parts = ct.split(";")
        content_type = parts[0]
        try:
            charset = parts[1].strip().lstrip('charset=')
        except IndexError:
            charset = None
        return content_type, charset

    def fetch(self, url, valid_content_types=None):
        """Requests the given URL and deals with any HTTP-related errors.

        Returns both an httplib2 Response object and the content."""
        # Default valid content types are generic XML or XML feed types
        if valid_content_types is None:
            valid_content_types = [ 
                'application/xml', 
                'text/xml',
                'application/atom+xml',
                'application/rss+xml',
                'application/rdf+xml'
            ]
        http_headers = { "User-Agent": config.BOT_USER_AGENT }
        # Setting this tells httplib2 to ignore its cache
        if config.HTTP_USE_CACHE == False:
            self.logger.debug("Skipping the httplib2 cache")
            http_headers['cache-control'] = 'no-cache'
        h = httplib2.Http(cache=config.CACHE_DIR)
        try:
            resp, content = h.request(url, method="GET", headers=http_headers)
        except IOError:
            # An IOError can happen, for example, when httplib2 can't write 
            # to its cache.
            # For now, just re-raise the exception.
            self.logger.error("IOError when fetching content!")
            raise
        # Deal with various HTTP error states
        if resp.status == 400:
            raise BadRequestError
        if resp.status == 401:
            raise NotAuthorizedError
        if resp.status == 403:
            raise URLForbiddenError
        if resp.status == 404:
            raise URLNotFoundError
        if resp.status == 410:
            raise URLGoneError
        if resp.status == 500:
            raise InternalServerError
        if resp.status == 502:
            raise BadGatewayError
        if resp.status == 503:
            raise ServiceUnavailableError
        # Bail if proper content-type not given
        content_type, charset = self._parse_content_type(resp['content-type'])
        if content_type in valid_content_types:
            # Weird: using not in the above test doesn't work
            pass
        else:
            msg = "Unsupported HTTP Content-Type: '%s'" % content_type
            self.logger.error(msg)
            raise UnsupportedContentTypeError(msg)
        self.http_response = resp
        self.http_content = content

    def parse(self): pass

def main():
	pass

if __name__ == '__main__':
	main()

