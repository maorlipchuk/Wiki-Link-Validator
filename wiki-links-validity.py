#!/usr/bin/env python

import ConfigParser
import fnmatch
import httplib
import logging
import os
import re
import sendMail
import shlex
import subprocess
import sys
from urlparse import urlparse

class ValidateWikiLinks():

    # Get all configuration values
    configParser = ConfigParser.RawConfigParser()
    configFilePath = 'conf/wiki.conf'
    configParser.read(configFilePath)
    home_dir = configParser.get('wiki-links-validator', 'HOME_DIR')
    file_prefix = configParser.get('wiki-links-validator', 'FILE_PREFIX')
    http_pattern = configParser.get('wiki-links-validator', 'HTTP_PATTERN')
    http_pattern2 = configParser.get('wiki-links-validator', 'HTTP_PATTERN2')
    invalid_http_codes = configParser.get('wiki-links-validator', 'INVALID_HTTP_CODES')
    http_url_whitelist = configParser.get('wiki-links-validator', 'URL_WHITELIST').split(',')
    should_send_mail = configParser.get('wiki-links-validator', 'SEND_MAIL')
    debug_log = configParser.get('wiki-links-validator', 'DEBUG_LOG')
    rot_links_log = configParser.get('wiki-links-validator', 'ROT_LINKS_LOG')

    # pre-configured yes/no answer for sending mail to author about broken link.
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])


    # Regex pattern for http.
    http_reg_pattern = re.compile(http_pattern)
    http_reg_pattern2 = re.compile(http_pattern2)

    # Formatter for log files.
    formatter=logging.Formatter('%(asctime)s %(message)s')

    def _init_log(self, log, log_name, level):
        hdlr=logging.FileHandler(log_name)
        hdlr.setFormatter(self.formatter)
        log.addHandler(hdlr)
        log.setLevel(level)


    def _config_logs(self):
        # Config debug log.
        self.log = logging.getLogger(self.debug_log)
        self._init_log(self.log, self.debug_log, logging.DEBUG)

        self.links_log = logging.getLogger(self.rot_links_log)
        self._init_log(self.links_log, self.rot_links_log, logging.ERROR)


    def _print_error_log(self, error_log):
        self.links_log.error(error_log)
        self.log.error(error_log)


    def _print_error_http_link(self, file_name, http_res, i, line, match, url, source):
        error_log = '\n Web page: %s\n line: %s [%d-%d]\n URL: %s\n Returned response code: %s\n' \
        % (source, i+1, match.start(0), match.end(0), url, http_res)
        self._print_error_log(error_log)


    def validate_links(self):
        # Config logs.
        self._config_logs()

        # Gather all files with file_prefix in matches.
        matches = []
        self.scan_files(matches, self.home_dir, self.file_prefix, self.log)
        self.files_scanned = 0

        # For each file check the URL.
        map(self.file_crawler, matches)


    def scan_files(self, matches, home_dir, file_prefix, log):
        self.log.info("Scan directory %s for the follwing file types %s " % (home_dir, file_prefix))
        self.qnt_files=0
        for root, dirnames, filenames in os.walk(home_dir):
            for filename in fnmatch.filter(filenames, file_prefix):
                self.qnt_files += 1
                self.log.debug("Match file: %s " % filename)
                matches.append(os.path.join(root, filename))
        self.log.info("\nNumber of files to scan: %i\n" , self.qnt_files)


    def file_crawler(self, file_name):
        self.files_scanned += 1
        self.log.info('Crawl into: %s [%i/%i]' % (file_name[len(self.home_dir):], self.files_scanned, self.qnt_files))
        for line_num, line in enumerate(open(file_name)):
            self.log.info("line number %s. line is: %s" % (line_num, line))
            self.line_crawler(line_num, line, file_name)


    def line_crawler(self, line_num, line, file_name):
        match = re.search(self.http_reg_pattern, line)
        if match:
            url = match.group(0)
            self.log.info("Found a match url (before second pattern): %s", url)
            match = re.search(self.http_reg_pattern2, url)
            if match:
                self.log.info("Found a match %s", match)
                self.validate_url(match, line_num, line, file_name)


    def validate_url(self, match, line_num, line, file_name):
        url = match.group(0)
        self.log.info('Validate http link found in line %s: %s' % (line_num+1, url))
        #self.log.info("White list is : %s", self.http_url_whitelist)
        #for str2 in self.http_url_whitelist:
        #    self.log.info("str: %s", str2)
        #    self.log.info("url: %s", url)
        if any(valid_url in url for valid_url in self.http_url_whitelist):
            self.log.info('Url %s is in the whitelist. Skipping validation' % url)
            return
        p = urlparse(url)
        source_file_from_repo = file_name[len(self.home_dir):]
        try:
            c = httplib.HTTPConnection(p.netloc)
            c.request("HEAD", p.path)
            http_res = str(c.getresponse().status)
            if (http_res in self.invalid_http_codes):
                self._print_error_http_link(file_name, http_res, line_num, line, match, url, source_file_from_repo)

                # Print the committer details.
                commit_hash, name, email, subject = self._fetch_commiter_info_from_git(url, line_num, source_file_from_repo)
                self.send_mail(commit_hash, name, email, subject, http_res, line_num, url, source_file_from_repo)
            else:
                self.log.info('\n Web page: %s\n line: %s\n URL: %s\n Returned response code: %s'\
                % (source_file_from_repo, line_num+1, url, http_res))
        except Exception as e:
            internal_err = '\n Internal Error!!! %s.\n Web page: %s\n line: %s [%d-%d]\n URL: %s'\
                % (e, source_file_from_repo, line_num+1, match.start(0), match.end(0), url)
            self._print_error_log(internal_err)

            # Print the committer details.
            commit_hash, name, email, subject = self._fetch_commiter_info_from_git(url, line_num, source_file_from_repo)
            self.send_mail(commit_hash, name, email, subject, "INVALID", line_num, url, source_file_from_repo)


    def send_mail(self, commit_hash, name, email, subject, http_res, line_num, url, source_file_from_repo):
        self.log.info(self.should_send_mail)
        if self.should_send_mail == 'True':
            msg = ("Hi %s,\n\n"
                   "It appears that the following http link is broken:\n"
                   "    URL: %s\n"
                   "    Returned response code: %s\n"
                   "    Source page: %s\n"
                   "    line: %s\n\n"
                   "According to the git repository this URL was first introduced in the following commit:\n"
                   "    Hash Code: %s\n"
                   "    Subject: %s\n\n"
                   "Please take a look and if needed provide a proper fix.\n\n Thank you") \
                  % (name, url, http_res, source_file_from_repo, line_num, commit_hash, subject)

            self.log.info(msg)
            should_send_mail = self._should_send_mail(msg, name)
            if should_send_mail:
                sendMail.send_mail(msg, email)
                sys.stdout.write("Mail sent successfully\n\n")
        else:
            self.log.debug("send mail flag is disabled")

    def _should_send_mail(self, msg, name, default='y'):
        message = "\n\n%s\n\nDo you want to send the above email to %s:\n" % (msg, name)
        choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
        choice = raw_input("%s (%s) " % (message, choices))
        values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
        return choice.strip().lower() in values

        choice = raw_input().lower()
        if choice in self.yes:
            return True
        elif choice in self.no:
            return False
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'")

    def _fetch_commiter_info_from_git(self, url, i, source):
        # Use git command to get the first appearance of the URL in the source code.
        # C - The home direcotory where the git repository is.
        # S - Indicates the string to grep in the code. The first apperance of the URL.
        # L - Searching the URL only on the source file in the line "line begin,line end:source file
        # %an - The name of the commiter, %aE - The email of the commiter, %s - The commit message.
        git_command = 'git -C %s log --reverse -S%s --pretty=format:\"%%an||%%aE||%%s||%%H||\" -L %s,%s:%s' % (self.home_dir, url, i+1, i+1, source)
        p = subprocess.Popen(shlex.split(git_command), stdout=subprocess.PIPE)
        retcode = p.wait()
        out, err = p.communicate()
        self.log.debug('Fetched commit using the following command : %s\n Output is: %s\n Error: %s' % (git_command, out, err))
        name, email, message, commit_hash, commit_params = out.split("||", 4)
        git_commit_params = '\n Commit Hash: %s\n Name: %s\n Email: %s\n Subject Message: %s\n\n\n\n' %(commit_hash, name, email, message)
        self._print_error_log(git_commit_params)
        return commit_hash, name, email, message


    def __init__(self):
        self.validate_links()


if __name__ == '__main__':
    ValidateWikiLinks()

