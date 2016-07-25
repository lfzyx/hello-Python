#!/usr/bin/env python3
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart,MIMEBase
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def mail(from_addr, to_addr, smtp_server, password, file, subject):
    msg = MIMEMultipart()
    msg['From'] = _format_addr(from_addr)
    msg['To'] = _format_addr(to_addr)
    msg['Subject'] = Header(subject, 'utf-8').encode()

    with open(file, 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('application', 'octet-stream', filename=file)
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename=file)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)

    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
