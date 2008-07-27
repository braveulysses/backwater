<?xml version="1.0" encoding="utf-8"?>

<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en">
    <title type="text">chompy.net</title>
    <link rel="alternate" type="text/html" href="http://chompy.net/"/>
    <link rel="self" type="application/atom+xml" href="http://chompy.net/feeds/index.atom"/>
    <updated>${now}</updated>
    <subtitle>more rocks and garbage</subtitle>
    <id>tag:chompy.net,2008://1</id>
    <generator>${generator}</generator>
    <rights>SNF Labs has asserted the moral right of the author of each post to be identified as the author of that post.</rights>
% for entry in entries:
    <entry>
% if entry.title is None or entry.title == '':
        <title type="text">untitled</title>
% else:
        <title type="html">${entry.title | x}</title>
% endif
        <link rel="alternate" type="text/html" href="${entry.url}"/>
% if entry.via is not None:
        <link rel="via" type="text/html" href="${entry.via}"/>
% endif
% if entry.comments is not None:
        <link rel="related" type="text/html" href="${entry.comments}"/>
% endif
        <published>${entry.published_atom}</published>
        <updated>${entry.updated_atom}</updated>
        <id>${entry.id}</id>
% if entry.summary != '':
    % if entry.type == 'quote':
        <summary type="text">"${entry.summary | x}"</summary>
    % else:
        <summary type="text">${entry.summary | x}</summary>
    % endif
% endif
% if entry.content != '' and entry.content != entry.summary:
    % if entry.type == 'quote':
        <content type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml">"${entry.content | x}"</div></content>
    % else:
        <content type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml">${entry.content | x}</div></content>
    % endif
% elif entry.summary == '' and entry.content == '':
        <content type="text/html" src="${entry.url}"/>
% endif
        <author>
            <name>${entry.author}</name>
% if entry.author_url is not None:
            <uri>${entry.author_url}</uri>
% endif
        </author>
% if entry.atom_source is not None:
        <source>
            <id>${entry.atom_source.id}</id>
            <title>${entry.atom_source.title | x}</title>
            <link rel="self" href="${entry.atom_source.url}"/>
            <updated>${entry.atom_source.updated}</updated>
        </source>
% endif
    </entry>
% endfor
</feed>