#!/usr/bin/env python3
import datetime
import os.path
import glob


def filelist(duration_days, files):
    duration_days = duration_days.split('-')

    today = datetime.date.today()
    firstday = today - datetime.timedelta(days=int(duration_days[-1]))
    lastday = today - datetime.timedelta(days=int(duration_days[0]))

    file_list = []

    for log_file in glob.glob(files):
        if firstday <= datetime.date.fromtimestamp(os.path.getmtime(log_file)) <= lastday:
            file_list.append(log_file)

    return file_list


