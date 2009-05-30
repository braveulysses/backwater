# backwater #

_We're all talking_

_To keep the conversation alive_

Backwater aggregates activity from Atom/RSS feeds, Twitter status feeds, 
Tumblr blogs, and Flickr photostreams.  Input is sanitized and output in 
valid, standards-compliant HTML 5 and Atom.

It has been used for some time to update the site
[chompy.net](http://chompy.net/).

## Usage ##

Running backwater without arguments will cause it to fetch and 

    python backwater.py

By default, backwater will use the sources defined in *sources.yaml*.

Output is stored in _data/output_.
Logs are stored in _data/logs_.
Caches are stored in _data/cache_.

Configuration can be adjusted by edited *config.py*.
The *--help* switch will list other options.

	$ python backwater.py --help
	Usage: python backwater.py
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

A couple of these haven't been implemented yet.

## Dependencies ##

* [httplib2](http://code.google.com/p/httplib2/)
* [Feed Parser](http://feedparser.org/)
* [Python FlickrAPI](http://flickrapi.sourceforge.net/)
* [python-twitter](http://code.google.com/p/python-twitter/)
* [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)
* [Mako](http://www.makotemplates.org/)
* [Smartypants](http://web.chad.org/projects/smartypants.py/)
* [Typogrify](http://code.google.com/p/typogrify/)
* [PyYAML](http://pyyaml.org/wiki/PyYAML)
* [TumblrAPI](https://github.com/cobralibre/tumblr-api/tree)

A modififed version of Typogrify is included. Other dependencies should be 
installable using *easy\_install*.

## License ##

???