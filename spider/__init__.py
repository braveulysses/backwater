import socket
import httplib2
import logging
import config

class BackwaterNetworkError(Exception): pass
class BackwaterHTTPError(BackwaterNetworkError): pass
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

module_logger = logging.getLogger("backwater.spider")

def parse_content_type(ct):
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

def fetch(url, valid_content_types=None):
    """Requests the given URL and throws HTTP errors left and right.

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
    # Setting HTTP_USE_CACHE to false tells httplib2 to ignore its cache
    if config.HTTP_USE_CACHE == False:
        module_logger.debug("Skipping the httplib2 cache")
        http_headers['cache-control'] = 'no-cache'
    h = httplib2.Http(cache=config.CACHE_DIR)
    try:
        resp, content = h.request(url, method="GET", headers=http_headers)
    except IOError:
        # An IOError can happen, for example, when httplib2 can't write 
        # to its cache.
        # For now, just re-raise the exception. If it happens, it's bad.
        module_logger.critical("IOError when fetching content!")
        raise
    except socket.error, e:
        module_logger.warning("Socket error while fetching '%s': '%s'" % (url, e))
        raise BackwaterNetworkError()
    except httplib2.ServerNotFoundError, e:
        module_logger.warning("Server not found: '%s'" % e)
        raise BackwaterNetworkError()
    # Throw exceptions for various HTTP error codes
    if resp.status == 400:
        raise BadRequestError
    elif resp.status == 401:
        raise NotAuthorizedError
    elif resp.status == 403:
        raise URLForbiddenError
    elif resp.status == 404:
        raise URLNotFoundError
    elif resp.status == 410:
        raise URLGoneError
    elif resp.status > 400 and resp.status < 500:
        raise BackwaterHTTPError
    elif resp.status == 500:
        raise InternalServerError
    elif resp.status == 502:
        raise BadGatewayError
    elif resp.status == 503:
        raise ServiceUnavailableError
    elif resp.status > 500 and resp.status < 600:
        raise BackwaterHTTPError
    # Bail if proper content-type not given
    content_type, charset = parse_content_type(resp['content-type'])
    if content_type in valid_content_types:
        # Weird: using 'not' in the above test doesn't work
        pass
    else:
        msg = "Unsupported HTTP Content-Type: '%s'" % content_type
        module_logger.error(msg)
        raise UnsupportedContentTypeError(msg)
    return resp, content

def update(sources):
    all_entries = []
    for src in sources:
        # Spider and parse sources
        try:
            module_logger.info("Parsing '%s'" % src.name)
            src.parse()
            src.normalize()
            for entry in src.entries:
                entry.normalize()
                all_entries.append(entry)
        except UnsupportedContentTypeError, err:
            module_logger.exception(err)
        except BackwaterHTTPError:
            module_logger.exception("HTTP error occurred!")
        except BackwaterNetworkError:
            module_logger.exception("Network error occurred!")
    return all_entries
