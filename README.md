# WikiLinksValidator
One of the most irritating things that can happen to you when going over a wiki is to find out a link in this wiki is not working.
The WikiLinksValidator is a project designed for wiki projects for validating links.

WikiLinksValidator is a script that goes over all the files with a pre-defined prefix,
and searches in the text, for a specific pattern, using regex, that contains a link.
Once a link has been found it validate it and print an appropriate log.

CONFIGURATION

The root directory of the project which we search all files:
* HOME_DIR = '/home/someone/ovirt-site/'

The file prefix of the files we want to scan:
* FILE_PREFIX = '*.html.md'

The link pattern in regex [](). It should be [Name of the link](The link it self):
* LINK_PATTERN = '\[(.*)\]\((.*)\)'

A regex for http pattern:
* HTTP_PATTERN = '(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'

Location of log file:
* DEBUG_LOG = '/home/user/ovirt-site/links.log'


