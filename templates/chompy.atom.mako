<?xml version="1.0" encoding="utf-8"?>

<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en">
    <title>chompy.net</title>
    <link rel="alternate" type="text/html" href="http://chompy.net/"/>
    <link rel="self" type="application/atom+xml" href="http://chompy.net/feeds/index.atom"/>
    <updated>${now}</updated>
    <subtitle>more rocks and garbage</subtitle>
    <id>tag:chompy.net,2008://1</id>
    <generator>${generator}</generator>
    <rights>Copyrights are retained by individual authors.</rights>
% for entry in entries:
    <entry>
% if entry.title is None or entry.title == '':
        <title>untitled</title>
% else:
        <title>${entry.title | x}</title>
% endif
        <link rel="alternate" type="text/html" href="${entry.url}"/>
        <published>${entry.published_atom}</published>
        <updated>${entry.updated_atom}</updated>
        <id>${entry.id}</id>
        <summary type="text">${entry.summary | x}</summary>
% if entry.content != '':
        <content type="text/html"><div>${entry.content | x}</div></content>
% endif
        <author>
            <name>${entry.author}</name>
        </author>
    </entry>
% endfor
</feed>