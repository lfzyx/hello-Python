#!/usr/bin/env python3
# author lfzyx date 2016.05.28

import sys
import zipfile
import glob
import os.path
import time
import subprocess
import configparser

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

# 用 jenkins 产生的 jar 包会有时间命名，为了避免冲突，删除旧的 jar 包
for jarfile in glob.glob(os.path.join(docBase, project, 'WEB-INF/lib/') + '*.jar'):
    os.remove(jarfile)

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
    time.sleep(5)            
    subprocess.check_call(os.path.join(rootpath, tomcat_T, project, "bin/startup.sh"))
    if count_of_project > 0:
        time.sleep(50)
