<!DOCTYPE html>

<html lang="en">

<head>
<meta charset="UTF-8">
<title>chompy.net</title>
<meta name="author" content="SNF Labs">
<meta name="description" content="the Spaceship No Future annex" />
<link rel="stylesheet" type="text/css" href="http://chompy.net/css/chompy-jul2008.css" title="Chompy" media="screen,projection" />
<link rel="feed" type="application/atom+xml" title="chompy.net feed" href="/feeds/chompy.atom" />
</head>

<body>
	
<section id="container">
	
<section id="content">

<header>
<h1>This is chompy.net, a part of Spaceship No Future.</h1>
</header>

<ul id="entries">
% for entry in entries:
% if entry.type == 'post':
## Post
<li class="post">
<h2><a href="${entry.url}">${entry.title}</a></h2>
<article>${entry.content}</article>
<p class="posted"><a href="${entry.source_url}">${entry.source_name}</a> &#183; <span class="timestamp">${entry.date}</span></p>
</li>

% elif entry.type == 'link':
## Link
<li class="link">
<h2><a href="${entry.url}">${entry.title}</a></h2>
<article>${entry.summary}</article>
<p class="posted"><a href="${entry.source_url}">${entry.source_name}</a> &#183; <span class="timestamp">${entry.date}</span></p>
</li>

% elif entry.type == 'quote':
## Quote
<li class="quote">
<article>
<blockquote cite="">
<p><a href="${entry.url}"><span class="dquo">&#8220;</span>${entry.summary}&#8221;</a></p>
</blockquote>
</article>
</li>

% elif entry.type == 'photo':
## Photo
<li class="photo">
<article>
<a href="${entry.url}"><img src="${entry.photo_url}" alt="" title="" height="" width="" /></a>
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
</footer>

</section>

</body>

</html>