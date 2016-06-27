# WikiLinkValidator - Validate URL links in your wiki.
A python tool designed for validating URLs as part of your wiki content, that is managed in a git repository.
![](/images/Introducing.gif)

## Description
One of the most annoying things that you might encounter while going over a wiki page, is to find out a link in it redirects you to a missing page (404).

Wiki-Validator uses a python script that scans all the files matching a pre-defined prefix,
and searches, using regex, for a specific pattern in the text that contains a link.
Once a link has been found it validate it and print an appropriate log.

## SETUP
* Make sure <i>python</i> and <i>git</i> are installed on your env.

* Clone your wiki git repo as so : `git clone git@github.com:{any wiki project}.git`
  
  For example, this is how we clone ovirt-site:
  ``` 
  git clone git@github.com:oVirt/ovirt-site.git
  ```

* Once your wiki project is cloned, set the home directory at conf/wiki.conf ![](/conf/wiki.conf):
```
   HOME_DIR = '/your_git_repo_location/'
```

* If you also want to send a mail to the author that introduced that rot link, set the SEND_MAIL option to true at /conf/wiki.conf ![conf/wiki.conf](/conf/wiki.conf):
```
   HOME_DIR = 'SEND_MAIL = 'True'
```

* There are other configuration values that can File prefix of the files we want to scan:
>FILE_PREFIX = '*.html.md'

The link pattern in regex [](). It should be the Name of the link in the (The link it self):
>LINK_PATTERN = '\[(.*)\]\((.*)\)'

A regex for http pattern:
>HTTP_PATTERN = (https?:\/\/(?:\www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})

Location of log file:
>DEBUG_LOG = '/home/user/ovirt-site/links.log'

## USAGE

