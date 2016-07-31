#!/usr/bin/env python3
import datetime
import os.path
import csv
import sys
import gzip
import configparser
import filelist_by_duration_days
import mail_attachment


if len(sys.argv) < 4:
    print("Usage:", sys.argv[0], "[mail_config]","[Spider]", "[duration_days]",)
    sys.exit(1)
# mail_config = "mail.conf"
# Spider = "Baiduspider/2.0"
# duration_days = "12-20"
mail_config = sys.argv[1]
Spider = sys.argv[2]
duration_days = sys.argv[3]

logfilelist = filelist_by_duration_days.filelist(duration_days, "/Users/lfzyx/git/python-simpletool/*")

csvfile = str(datetime.date.fromtimestamp(os.path.getmtime(logfilelist[-1])))+'-'+str(datetime.date.fromtimestamp(os.path.getmtime(logfilelist[0])))+'.csv'

with open(csvfile, 'a', newline='') as openfile:
    for logfile in reversed(logfilelist):
        with gzip.open(logfile , "rb")  as file:
            spamwriter = csv.writer(openfile, dialect='excel')
            spamwriter.writerow(" ")
            for line in file:
                line = line.decode('ascii')
                if("Baiduspider/2.0" in line):
                    _list = line.split(' ')
                    spamwriter.writerow([_list[3][1:], _list[6]])

#邮件配置
class Config:
    def __init__(self, mail_config):
        self.config_path = mail_config
        self.cc = configparser.ConfigParser()
        self.cc.optionxform = str
        self.cc.read(self.config_path)

    def __str__(self):
        return self.config_path

    def __get_sections__(self):
        return self.cc.sections()  # 读取每个配置项

    def __get_optons__(self, sections):
        return self.cc.options(sections)  # 读取配置项中的属性列表

    def __get_items__(self, sections, options):
        return self.cc.get(sections, options)  # 读取属性对应的值

config = Config(mail_config)
from_addr = config.__get_items__("smtp", "from_addr")
password = config.__get_items__("smtp", "password")
to_addr = config.__get_items__("smtp", "to_addr")
smtp_server = config.__get_items__("smtp" , "smtp_server")


mail_attachment.mail(from_addr, to_addr, smtp_server, password, csvfile, "百度爬虫轨迹")