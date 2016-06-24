#!/usr/bin/env python
import logging
import logging.handlers
import ConfigParser


class TlsSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        """
        Emit a record.
        Format the record and send it to the specified addresses.
        """
        try:
            import smtplib
            import string  # for tls add this line
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            string.join(self.toaddrs, ","),
                            self.getSubject(record),
                            formatdate(), msg)
            if self.username:
                smtp.ehlo()  # for tls add this line
                smtp.starttls()  # for tls add this line
                smtp.ehlo()  # for tls add this line
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


# Get all configuration values
configParser = ConfigParser.RawConfigParser()
configFilePath = 'conf/mail.conf'
configParser.read(configFilePath)

mailhost = configParser.get('mail-wiki-links-validator', 'MAILHOST')
port = configParser.get('mail-wiki-links-validator', 'PORT')
subject = configParser.get('mail-wiki-links-validator', 'SUBJECT')
fromaddr = configParser.get('mail-wiki-links-validator', 'FROMADDR')
username = configParser.get('mail-wiki-links-validator', 'USERNAME')
password = configParser.get('mail-wiki-links-validator', 'PASSWORD')


def send_mail(msg, toaddr):
    logger = logging.getLogger("mail")
    addr = 'mlipchuk@redhat.com'
    gm = TlsSMTPHandler((mailhost, port), fromaddr, addr,
                        subject, (username, password))
    logger.addHandler(gm)
    logger.log(logging.ERROR, msg)
    logger.removeHandler(gm)
