#!/usr/bin/env python3
# Author: lfzyx
# Contact: lfzyx.me@gmail.com
"""
list files by days to days

import list_files_by_days
list_files_by_days.filelist(3 20 Downloads/*)

"""
import datetime
import os.path
import glob
import sys


def days(firstday, lastday):
    """
    return the day in datetime.date format (year, month, day)
    """
    today = datetime.date.today()
    firstdate = today - datetime.timedelta(days=int(lastday))
    lastdate = today - datetime.timedelta(days=int(firstday))

    return firstdate, lastdate


def filelist(firstday, lastday, files):
    """
    return the file that modify time status < lastdate and > firstdate
    """
    firstdate, lastdate = days(firstday, lastday)
    file_list = []

    for log_file in sorted(glob.glob(files), key=os.path.getmtime):
        if firstdate <= datetime.date.fromtimestamp(os.path.getmtime(log_file)) <= lastdate:
            file_list.append(log_file)

    return file_list


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage:", sys.argv[0], "firstday", "lastday", "files")
        print("Example: 3 20 Downloads/*")
        sys.exit(1)

    print(filelist(sys.argv[1], sys.argv[2], sys.argv[3]))
