#!/usr/bin/env python3
# author lfzyx date 2016.09.14

import sys
import zipfile
import glob
import os.path
import time
import subprocess
import configparser
import shutil

if len(sys.argv) < 4:
    print("Usage:", sys.argv[0], "[config_path]", "[project]", "[tomcat]..")
    sys.exit(1)

config_path = sys.argv[1]
project = sys.argv[2]
tomcat = sys.argv[3:]
count_of_project = len(tomcat)

config = configparser.ConfigParser()
config.read(config_path)
rootpath = config.get("rootpath", "path")
docBase = config.get("docBase", "path")

# 用 jenkins 产生的 jar 包会有时间命名，为了避免冲突，删除旧的 jar 包
for jarfile in glob.glob(os.path.join(rootpath, docBase, project, 'WEB-INF/lib/') + '*.jar'):
    os.remove(jarfile)

warfile = zipfile.ZipFile(os.path.join(rootpath, docBase, project+".war", ))
warfile.extractall(os.path.join(rootpath, docBase, project))

for sections in config.sections():
    '''
    获取不同配置文件的路径，然后把源复制到目标
    '''
    try:
        dstpath = config.get(sections, "dstpath")
        srcpath = config.get(sections, "srcpath")
    except (configparser.Error,):
        print(sys.exc_info()[1])
        print("如果异常与 rootpath docBase 有关，那就没事了")
    else:
        try:
            shutil.copy(os.path.join(srcpath, sections), os.path.join(dstpath, sections))
        except (shutil.Error, IsADirectoryError, FileNotFoundError):
            print(sys.exc_info()[1])
        else:
            print("Move %s successful" % (sections,))

# 重启 tomcat 集群
for tomcat_T in tomcat:
    count_of_project -= 1
    subprocess.check_call(os.path.join(rootpath, tomcat_T, project, "bin/shutdown.sh"))
    time.sleep(5)
    subprocess.check_call(os.path.join(rootpath, tomcat_T, project, "bin/startup.sh"))
    if count_of_project > 0:
        time.sleep(50)
