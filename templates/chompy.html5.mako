<%!
	from publish.typogrify import amp
	from publish.typogrify import caps
	from publish.typogrify import initial_quotes
	from publish.typogrify import smartypants
	from publish.typogrify import widont
	from publish.typogrify import typogrify
%>\
<!DOCTYPE html>

<html lang="en">

<head>
<meta charset="UTF-8">
<title>chompy.net</title>
<meta name="viewport" content="width=700">
<meta name="generator" content="${generator}">
<meta name="author" content="SNF Labs">
<meta name="description" content="the Spaceship No Future annex" />
<link rel="stylesheet" type="text/css" href="${base_url}/css/chompy-jul2008.css" title="Chompy" media="screen,projection" />
<link rel="feed" type="application/atom+xml" title="chompy.net feed" href="${feeds_url}/chompy.atom" />
</head>

<body>
	
<section id="container">
	
<section id="content">

<header>
<div>
<h1>This is <a href="http://chompy.net/">chompy.net</a>, a part of <a href="http://www.spaceshipnofuture.org">Spaceship No Future</a>.</h1>
</div>
</header>

<ul id="entries">
% for entry in entries:
% if entry.type == 'post':
## Post
<li class="post">
<h2><a href="${entry.url | h}">${entry.title | typogrify}</a></h2>
<article>${entry.content_abridged | typogrify}</article>
<p class="posted"><a href="${entry.source_url | h}">${entry.source_name}</a> &#183; <span class="timestamp">${entry.published_formatted}</span></p>
</li>

% elif entry.type == 'link':
## Link
<li class="link">
<h2><a href="${entry.url | h}">${entry.title | typogrify}</a></h2>
<article>
${entry.summary | typogrify}
% if entry.comments is not None:
 <a href="${entry.comments | h}" class="comments">(#)</a>
% endif
% if entry.via is not None:
 <a href="${entry.via | h}" class="via">(via)</a>
% endif
</article>
<p class="posted"><a href="${entry.source_url | h}">${entry.source_name}</a> &#183; <span class="timestamp">${entry.published_formatted}</span></p>
</li>

% elif entry.type == 'quote':
## Quote
<li class="quote">
<article>
<blockquote>
<p><a href="${entry.url | h}"><span class="dquo">&#8220;</span>${entry.summary | amp,caps,smartypants}&#8221;</a></p>
</blockquote>
</article>
</li>

% elif entry.type == 'photo':
## Photo
<li class="photo">
<article>
% if entry.photo_type == 'flickr':
<a href="${entry.url | h}"><img src="${base_url}${entry.cached_url}" alt="${entry.title}" title="'${entry.title},' by ${entry.author}" height="${entry.height}" width="${entry.width}" /></a>
% else:
<a href="${entry.url | h}"><img src="${base_url}${entry.cached_url}" alt="" height="${entry.height}" width="${entry.width}" /></a>
% endif
</article>
</li>

% elif entry.type == 'song':
## Song
<li class="song">
</li>

% elif entry.type == 'video':
## Video
<li class="video">
</li>

% elif entry.type == 'conversation':
## Conversation
##
## Use <dialog> to mark up Conversations.
##    <dialog>
##      <dt>Waki
##      <dd>What sort of fruit have you there?
##      <dt>Tsure
##      <dd>I've nuts and kaki and chestnuts and plums and peaches.
##    </dialog>
<li class="conversation">
</li>
% endif
% endfor
</ul>

</section>

<footer>
<div>
<p id="labs">
Brought to you by <span class="caps snf">SNF</span> Labs.
</p>
<p>
<img src="http://chompy.net/images/tankcat_mini.gif" height="72" width="90" alt="SNF IS REAL" />
</p>
</div>
</footer>

</section>

<!-- Google Analytics tracking code -->

<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
var pageTracker = _gat._getTracker("UA-3678757-3");
pageTracker._initData();
pageTracker._trackPageview();
</script>

</body>

</html>
