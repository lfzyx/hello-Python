#!/usr/bin/env python3
import datetime
import os.path
import glob
import sys


def filelist(duration_days, files):
    duration_days = duration_days.split('-')

    today = datetime.date.today()
    firstday = today - datetime.timedelta(days=int(duration_days[-1]))
    lastday = today - datetime.timedelta(days=int(duration_days[0]))

    file_list = []

    for log_file in sorted(glob.glob(files), key=os.path.getmtime):
        if firstday <= datetime.date.fromtimestamp(os.path.getmtime(log_file)) <= lastday:
            file_list.append(log_file)

    return file_list


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:", sys.argv[0], "duration_days", "files" )
        print("Example: 3-20 Downloads/*")
        sys.exit(1)
    print(filelist(sys.argv[1], sys.argv[2]))


