# backwater #

> _We're all talking_  
> _To keep the conversation alive_

Backwater aggregates activity from Atom/RSS feeds, Twitter status feeds, 
Tumblr blogs, and Flickr photostreams.  Input is sanitized and output in 
valid, standards-compliant HTML 5 and Atom.

It's not without problems, but has been in use for quite some time 
with the site [chompy.net](http://chompy.net/).

## Usage ##

Running backwater without arguments will cause it to fetch and process 
its sources, then spew out some output files.

    python backwater.py

By default, backwater will use the sources defined in *sources.yaml*.

Output is stored in _data/output_.
Logs are stored in _data/logs_.
Caches are stored in _data/cache_.

Configuration can be adjusted by editing *config.py*. 
Note that a handful of sensitive settings must be defined 
as environment variables.  These are:

* *BACKWATER\_FLICKR\_KEY*, your Flickr API key
* *BACKWATER\_TWITTER\_ACCOUNT*, a Twitter account wit access to any Twitter accounts that you plan to follow
* *BACKWATER\_TWITTER\_PASSWORD*, the system Twitter account's password

The easiest way to handle this is to define the above variables in a shell 
script which calls backwater.py.

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

Backwater is BSD-licensed.

Copyright (c) 2010, SNF Labs, Jacob Childress  
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of SNF Labs nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.