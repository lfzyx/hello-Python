#!/usr/bin/env python3
# author lfzyx date 2016.05.28

import sys
import os
import zipfile
import glob
import os.path
import shutil
import configparser
import time
import subprocess

if len(sys.argv) < 4:
    print("Usage:", sys.argv[0], "[config_path]", "[project]", "[tomcat]..")
    sys.exit(1)

config_path = sys.argv[1]  # deploy_tomcat.conf.sample
project = sys.argv[2]
tomcat = sys.argv[3:]
count_of_project = len(tomcat)

class Config:
    def __init__(self, config_path):
        self.config_path = config_path
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

config = Config(config_path)
docBase = config.__get_items__("docBase", "path")

# 用 jenkins 产生的 jar 包会有时间命名，为了避免冲突，删除旧的 jar 包
for jarfile in glob.glob(os.path.join(docBase, project, 'WEB-INF/lib/') + '*.jar'):
    os.remove(jarfile)

warfile = zipfile.ZipFile(os.path.join(docBase, project+".war", ))
warfile.extractall(os.path.join(docBase, project))

for sections in config.__get_sections__():
    '''
    根据不通的配置项打开工程中不通的配置文件，然后修改能匹配的配置项属性值
    '''
    temp = ""
    try:
        with open(os.path.join(docBase, project, config.__get_items__(sections, "path")), "r", encoding="utf-8") \
                as file:
            for line in file:
                _list = line.split('=')
                for item in config.__get_optons__(sections):
                    if (_list[0] == item):
                        _list[1] = config.__get_items__(sections, item)
                        line = _list[0] + '=' + _list[1] + '\n'
                temp += line
    except (IsADirectoryError, FileNotFoundError):
        print(sys.exc_info()[1])
    else:
        with open(os.path.join(docBase, project, config.__get_items__(sections, "path")), "w", encoding="utf-8") \
                as file:
            file.write(temp)

# 重启 tomcat 集群
for tomcat_T in tomcat:
    count_of_project -= 1
    subprocess.check_call(os.path.join(rootpath, tomcat_T, project, "bin/shutdown.sh"))
    time.sleep(5)            
    subprocess.check_call(os.path.join(rootpath, tomcat_T, project, "bin/startup.sh"))
    if count_of_project > 0 :
        time.sleep(50)
