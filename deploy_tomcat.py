#!/usr/bin/env python3
# author lfzyx date 2016.05.28

import sys
import zipfile
import datetime
import os.path
import time
import subprocess
import configparser
import psutil
import distutils.dir_util

if len(sys.argv) < 4:
    print("Usage:", sys.argv[0], "[config_path]", "[project]", "[tomcat]..")
    sys.exit(1)

config_path = sys.argv[1]  # deploy_tomcat.conf.sample
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
    distutils.dir_util.copy_tree(os.path.join(rootpath, docBase, project), os.path.join(rootpath, 'bakdocBase', dstname))
except:
    print(sys.exc_info()[1])
else:
    print("backup %s successful" % project)

# 为了避免冲突，删除旧的工程包
try:
    distutils.dir_util.remove_tree(os.path.join(rootpath, docBase, project))
except:
    print(sys.exc_info()[1])
else:
    print("delete old %s successful" % project)

warfile = zipfile.ZipFile(os.path.join(docBase, project+".war", ))
warfile.extractall(os.path.join(docBase, project))

for sections in config.sections():
    '''
    根据不通的配置项打开工程中不通的配置文件，然后修改能匹配的配置项属性值
    '''
    temp = ""
    try:
        with open(os.path.join(docBase, project, config.get(sections, "path")), "r", encoding="utf-8") \
                as file:
            for line in file:
                _list = line.split('=')
                for item in config.options(sections):
                    if _list[0] == item:
                        _list[1] = config.get(sections, item)
                        line = _list[0] + '=' + _list[1] + '\n'
                temp += line
    except (IsADirectoryError, FileNotFoundError):
        print(sys.exc_info()[1])
    else:
        with open(os.path.join(docBase, project, config.get(sections, "path")), "w", encoding="utf-8") \
                as file:
            file.write(temp)

# 重启 tomcat 集群
for tomcat_T in tomcat:
    count_of_project -= 1
    subprocess.check_call(os.path.join(rootpath, tomcat_T, project, "bin/shutdown.sh"))
    time.sleep(7)
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
        time.sleep(60)
