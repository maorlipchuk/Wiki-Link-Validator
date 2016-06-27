# WikiLinkValidator - Validate URL links in your wiki.
A python tool designed to validate URLs as part of the wiki content which is managed in a git repository.

![](/images/Introducing.gif)

A tool designed to validate http links in wiki projects.

One of the most annoying things that you might encounter while reading a wiki page, is to find out a link in it redirects you to a missing page (404).

Wiki-Validator uses a python script that scans all the files matching a pre-defined prefix,
and searches, using regex, for a specific pattern in the text that contains a link.
Once a link has been found it validate it and print an appropriate log.

## SETUP

Once your wiki project is cloned, set the home directory to search files from:
>HOME_DIR = '/home/someone/ovirt-site/'

The file prefix of the files we want to scan:
>FILE_PREFIX = '*.html.md'

The link pattern in regex [](). It should be the Name of the link in the (The link it self):
>LINK_PATTERN = '\[(.*)\]\((.*)\)'

A regex for http pattern:
>HTTP_PATTERN = (https?:\/\/(?:\www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})

Location of log file:
>DEBUG_LOG = '/home/user/ovirt-site/links.log'

## USAGE

