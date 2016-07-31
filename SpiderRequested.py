#!/usr/bin/env python3
# Author: lfzyx
# Contact: lfzyx.me@gmail.com
"""
通过输入第一天和最后一天,获取这段时间的日志文件.然后过滤出想要的 User Agent, 最后通过邮件发送生成的 csv 文件

"""
import datetime
import os.path
import csv
import sys
import gzip
import list_files_by_days
import send_mail

if len(sys.argv) < 6:
    print("Usage:", sys.argv[0], "mail_config", "Spider", "firstday", "lastday", "logfiles")
    print("Example: mail.conf Googlebot 3 20 'log/*' ")
    sys.exit(1)
mail_config = sys.argv[1]
Spider = sys.argv[2]
firstday = sys.argv[3]
lastday = sys.argv[4]
logfiles = sys.argv[5]


logfilelist = list_files_by_days.filelist(firstday, lastday, logfiles)

csvfile = str(datetime.date.fromtimestamp(os.path.getmtime(logfilelist[0])))+'-'+\
          str(datetime.date.fromtimestamp(os.path.getmtime(logfilelist[-1])))+'.csv'


with open(csvfile, 'a', newline='') as openfile:
    for logfile in logfilelist:
        with gzip.open(logfile , "rb")  as file:
            spamwriter = csv.writer(openfile, dialect='excel')
            spamwriter.writerow(" ")
            for line in file:
                line = line.decode('ascii')
                if Spider in line:
                    _list = line.split(' ')
                    spamwriter.writerow([_list[3][1:], _list[6]])


send_mail.attachment_content(mail_config, Spider, [csvfile])


