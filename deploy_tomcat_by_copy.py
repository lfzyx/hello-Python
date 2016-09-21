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
import datetime
import psutil


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

# 备份之前的工程
dstname = "%s_%s" % (project, datetime.datetime.today().strftime("%Y%m%d%H%M"))
try:
    shutil.copytree(os.path.join(rootpath, docBase, project), os.path.join(rootpath, 'bakdocBase', dstname))
except:
    print(sys.exc_info()[1])
else:
    print("backup %s successful" % project)

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
    #检测tomcat是否关闭
    for proc in psutil.process_iter():
        pinfo = proc.as_dict(attrs=['pid', 'cmdline'])
        if pinfo["cmdline"]:
            for temp in pinfo["cmdline"]:
                if tomcat_T + "/" + project in temp:
                    try:
                        proc.kill()
                    except:
                        print(sys.exc_info()[1])
                    else:
                        print("kill Process", pinfo["pid"], tomcat_T, project)
                    finally:
                        break
    subprocess.check_call(os.path.join(rootpath, tomcat_T, project, "bin/startup.sh"))
    if count_of_project > 0:
        time.sleep(50)
