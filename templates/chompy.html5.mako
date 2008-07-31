<%!
    from publish.typogrify import amp
    from publish.typogrify import caps
    from publish.typogrify import initial_quotes
    from publish.typogrify import smartypants
    from publish.typogrify import widont
    from publish.typogrify import typogrify
    from publish.sanitizer import escape_amps_only
%><!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">

<head>
<title>chompy.net</title>
<meta name="viewport" content="width=700" />
<meta name="generator" content="${generator}/${generator_version}" />
<meta name="author" content="SNF Labs" />
<meta name="description" content="the Spaceship No Future annex" />
<link rel="stylesheet" type="text/css" href="${base_url}/css/chompy-jul2008.css" media="screen" />
<link rel="feed" type="application/atom+xml" title="chompy.net feed" href="${feeds_url}/chompy.atom" />
<link rel="alternate" type="application/atom+xml" title="chompy.net feed" href="${feeds_url}/chompy.atom" />
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<script type="text/javascript" src="/js/chompy.js"></script>
<script type="text/javascript">
    Chompy.html5_fix();
    if (document.addEventListener) {
        document.addEventListener('DOMContentLoaded', Chompy.inject_ga_script, false);
    } else if (document.attachEvent) {
        document.attachEvent('onload', Chompy.inject_ga_script);
    }
</script>
</head>

<body>
    
<div id="container">
    
<div id="content">

<header>
<div>
<h1>This is <a href="http://chompy.net/">chompy.net</a>, a part of <a href="http://www.spaceshipnofuture.org">Spaceship No Future</a>.</h1>
</div>
</header>

## TODO: Rejigger entry markup using Sam Ruby's HTML 5 markup as a model.
## See: <http://intertwingly.net/blog/>
<ul id="entries">
% for entry in entries:
% if entry.type == 'post':
## Post
<li class="post">
<h2><a href="${entry.url | h}">${entry.title | typogrify,escape_amps_only}</a></h2>
<article>${entry.content_abridged | typogrify,escape_amps_only}</article>
<p class="posted"><a href="${entry.source.url | h}">${entry.source.name}</a> &#183; <time datetime="${entry.published_atom}">${entry.published_formatted}</time></p>
</li>

% elif entry.type == 'link':
## Link
<li class="link">
<h2><a href="${entry.url | h}">${entry.title | typogrify,escape_amps_only}</a></h2>
<article>
${entry.content | typogrify,escape_amps_only}
% if entry.comments is not None:
 <a href="${entry.comments | h}" class="comments">(#)</a>
% endif
% if entry.via is not None:
 <a href="${entry.via | h}" class="via">(via)</a>
% endif
</article>
<p class="posted"><a href="${entry.source.url | h}">${entry.source.name}</a> &#183; <time datetime="${entry.published_atom}">${entry.published_formatted}</time></p>
</li>

% elif entry.type == 'quote':
## Quote
<li class="quote">
<article>
% if entry.via is not None:
<blockquote cite="${entry.via}">
% else:
<blockquote>
% endif
<p><a href="${entry.url | h}"><span class="dquo">&#8220;</span>${entry.content | amp,caps,smartypants,escape_amps_only}&#8221;</a></p>
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

</div> <!--/content -->

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

</div> <!--/container -->

</body>

</html>
