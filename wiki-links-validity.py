#!/usr/bin/env python

import fnmatch
import os
import re
import httplib
import logging
from urlparse import urlparse

### Pre-configured parameters. ###

# The root directory of the project which we search all files.
HOME_DIR = '$HOME/ovirt-site/'

# The file prefix of the files we want to scan
FILE_PREFIX = '*.html.md'

# The link pattern in regex [](). It should be [Name of the link](The link it self).
LINK_PATTERN = '\[(.*)\]\((.*)\)'

# A regex for http pattern
HTTP_PATTERN = '(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'

# Location of log file
DEBUG_LOG = '$HOME/ovirt-site/links.log'

logging.basicConfig(filename=DEBUG_LOG, level=logging.ERROR)

def validate_links():
    matches = []
    for root, dirnames, filenames in os.walk(HOME_DIR):
        for filename in fnmatch.filter(filenames, FILE_PREFIX):
            matches.append(os.path.join(root, filename))


    pattern = re.compile(LINK_PATTERN)
    http_pattern = re.compile(HTTP_PATTERN)
    for file_name in matches:
        logging.info('Validating file name %s' % (file_name[len(HOME_DIR):]))
        for i, line in enumerate(open(file_name)):
            for match in re.finditer(pattern, line):
                logging.debug('Found link in line %s: %s' % (i+1, match.groups()))
                url = match.group(2)
                for match_url in re.finditer(http_pattern, url):
                    logging.debug('Validating http url %s' % (match_url.groups()))
                    p = urlparse(url)
                    try:  
                        c = httplib.HTTPConnection(p.netloc)
                        c.request("HEAD", p.path)
                        http_res = int(c.getresponse().status)
                        if (http_res == 404) or (http_res == 500):
                            logging.error('Web page: %s\n line: %s\n URL: %s\n Returned response code: %d' % (file_name[len(HOME_DIR):], i+1, url, http_res))
                    except Exception as e:
                        print 'ERROR:Encountered an internal error validating Web site %s\n (wiki location: %s at line: %s' % (url, file_name, i+1)
                        logging.error('Internal Error!!! %s.\n Web page: %s\n line: %s\n URL: %s' % (e, file_name[38:], i+1, url))

validate_links()
