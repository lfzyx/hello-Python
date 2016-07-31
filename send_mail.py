#!/usr/bin/env python3
# Author: lfzyx
# Contact: lfzyx.me@gmail.com
"""
send mail with attachments

import send_mail
send_mail.attachment_content(mail.conf subject access.log.19.gz access.log.18.gz)

"""
import sys
import config
from email.mime import text, multipart, base
import email.encoders
import smtplib


def smtp_send(mail_config, msg):
    """
    send mail by smtp
    """

    configfile = config.Config(mail_config)

    smtp_server = configfile.__get_items__("smtp", "smtp_server")
    from_addr = configfile.__get_items__("smtp", "from_addr")
    password = configfile.__get_items__("smtp", "password")
    to_addr = configfile.__get_items__("smtp", "to_addr")

    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, password)
    server.send_message(msg, from_addr, [to_addr])
    server.quit()


def text_content(mail_config, subject):
    """
    create MIME objects of major type text by email.mime.text.MIMEText class
    """

    configfile = config.Config(mail_config)
    from_addr = configfile.__get_items__("smtp", "from_addr")
    to_addr = configfile.__get_items__("smtp", "to_addr")

    msg = text.MIMEText('<html><body><h1>lfzyx</h1><p>send by <a href="http://lfzyx.org">lfzyx</a></p>''</body></html>',
                        'html', 'utf-8')
    msg['To'] = to_addr
    msg['From'] = from_addr
    msg['Subject'] = subject

    smtp_send(mail_config, msg)


def attachment_content(mail_config, subject, files):
    """
    create base class for all the MIME-specific subclasses of Message by email.mime.base.MIMEBase class
    """

    configfile = config.Config(mail_config)
    from_addr = configfile.__get_items__("smtp", "from_addr")
    to_addr = configfile.__get_items__("smtp", "to_addr")

    msg = multipart.MIMEMultipart()
    msg['To'] = to_addr
    msg['From'] = from_addr
    msg['Subject'] = subject

    msg.attach(text.MIMEText('<html><body><p>send by <a href="http://lfzyx.org">lfzyx</a></p>''</body></html>',
                             'html', 'utf-8'))

    for file in files:
        with open(file, 'rb') as f:
            stream = base.MIMEBase('application', 'octet-stream', filename=file)
            stream.add_header('Content-Disposition', 'attachment', filename=file)
            stream.add_header('Content-ID', '<0>')
            stream.add_header('X-Attachment-Id', '0')
            stream.set_payload(f.read())
            email.encoders.encode_base64(stream)
            msg.attach(stream)

    smtp_send(mail_config, msg)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage:", sys.argv[0], "mail_config subject files")
        print("Example: mail.conf test access.log.19.gz access.log.18.gz")
        sys.exit(1)

    attachment_content(sys.argv[1],sys.argv[2],sys.argv[3:])

