#!/usr/bin/env python

import fnmatch
import os
import re
import httplib
import logging
import ConfigParser
from urlparse import urlparse


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


def main():
    configParser = ConfigParser.RawConfigParser()   
    configFilePath = 'wiki.conf'
    configParser.read(configFilePath)
    self.home_dir = configParser.get('wiki-links-validator', 'HOME_DIR')
    self.file_prefix = configParser.get('wiki-links-validator', 'FILE_PREFIX')
    self.link_pattern = configParser.get('wiki-links-validator', 'LINK_PATTERN')
    self.http_pattern = configParser.get('wiki-links-validator', 'HTTP_PATTERN')
    self.debug_log = configParser.get('wiki-links-validator', 'DEBUG_LOG')
    print "dsfdsf %s" % self.home_dir
    logging.basicConfig(filename=self.debug_log, level=logging.ERROR)
    #validate_links()

if __name__ == '__main__':
  main()
