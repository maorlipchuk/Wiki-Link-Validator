# WikiLinkValidator - Validate URL links in your wiki.
A python tool designed for validating URLs as part of your wiki content, that is managed in a git repository.
<p align="center"><img src ="/images/Introducing.gif" /></p>

## Description
One of the most annoying things you might encounter while going over a wiki page, is to find out a link in it redirects you to a missing page (404).

Wiki-Validator uses a python script that scans all the files matching a pre-defined prefix,
and searches, using regex, for a specific pattern in the text that contains a link.
Once a link has been found it validate it and print an appropriate log.

## SETUP
* Make sure <i>python</i> and <i>git</i> are installed on your env.

* Clone the wiki git repo you want to scan, as so : `git clone git@github.com:{any wiki project}.git`
  
  For example, this is how we clone ovirt-site:
  ``` 
  git clone git@github.com:oVirt/ovirt-site.git
  ```

* Once your wiki project is cloned, set the home directory at conf/[wiki.conf](/conf/wiki.conf):
```
   HOME_DIR = '/your_git_repo_location/'
```

* If you also want to add the ability to send a mail to the author which introduced that rot link, set the SEND_MAIL option to true in /conf/[wiki.conf](/conf/wiki.conf):
```
   SEND_MAIL = 'True'
```

* Once the util is running a report of all the rot links in the git repo will be published in a log file configured in  /conf/[wiki.conf](/conf/wiki.conf):
```
   ROT_LINKS_LOG=rot_links.log
```

## Other Useful Configuration Values

* Some URLs are used in the wiki to reflect an example or an internal link (like localhost).
Those types of URLs can be configured in the URL whitelist so those can be steped over and avoid validation.
The whitelist values are being checked against every link found in the git repo files, and if one link contains part of the string in the white list a proper message will be logged and this link will not be validated.
`URL_WHITELIST = yourhost.example.com,localhost

* The prefix of files to scan in the git repo for http links:
`FILE_PREFIX=*.html.md

* All the http return codes which reflect an invalid http page:
`INVALID_HTTP_CODES=

* The regex which is being used for http pattern:
`HTTP_PATTERN =

* Second HTTP_PATTERN regex to double check the URL link:
`HTTP_PATTERN2 =

* Location of the log file:
`DEBUG_LOG = '/home/user/ovirt-site/links.log'


