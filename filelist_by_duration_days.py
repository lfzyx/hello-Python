#!/usr/bin/env python3
import datetime
import os.path
import sys

if len(sys.argv) < 3:
    print("Usage:", sys.argv[0], "[duration days]", "[files]")  # 输入日期范围和文件路径,文件支持通配符
    print("example: filelist_by_duration_days.py 6-12 /var/log/authd*")
    sys.exit(1)

duration_days = sys.argv[1].split('-')
files = sys.argv[2:]

today = datetime.date.today()

firstday = today - datetime.timedelta(days=int(duration_days[-1]))
lastday = today - datetime.timedelta(days=int(duration_days[0]))

file_list = []

for log_file in files:
    if firstday <= datetime.date.fromtimestamp(os.path.getmtime(log_file)) <= lastday:
        file_list.append(log_file)


print(file_list)



