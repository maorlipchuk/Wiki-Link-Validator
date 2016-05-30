# Wiki-Validator
A tool, designed to validate links in wiki projects.
One of the most annoying things that you might encounter while reading a wiki page, is to find out a link in it redirects you to a missing page (404).

Wiki-Validator uses a python script that scans all the files matching a pre-defined prefix,
and searches, using regex, for a specific pattern in the text that contains a link.
Once a link has been found it validate it and print an appropriate log.

CONFIGURATION

The root directory of the project which we search all files:
* HOME_DIR = '/home/someone/ovirt-site/'

The file prefix of the files we want to scan:
* FILE_PREFIX = '*.html.md'

The link pattern in regex [](). It should be the Name of the link in the (The link it self):
* LINK_PATTERN = '\[(.*)\]\((.*)\)'

A regex for http pattern:
* HTTP_PATTERN = "(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})"

Location of log file:
* DEBUG_LOG = '/home/user/ovirt-site/links.log'


