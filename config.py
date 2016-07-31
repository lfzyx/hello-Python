#!/usr/bin/env python3
# Author: lfzyx
# Contact: lfzyx.me@gmail.com
"""
the class use to get config sections, options, items

"""
import configparser


class Config:
    def __init__(self, file):
        self.configfile = file
        self.cc = configparser.ConfigParser()
        self.cc.optionxform = str
        self.cc.read(self.configfile)

    def __str__(self):
        return self.configfile

    def __get_sections__(self):
        return self.cc.sections()  # 读取每个配置项

    def __get_options__(self, sections):
        return self.cc.options(sections)  # 读取配置项中的属性列表

    def __get_items__(self, sections, options):
        return self.cc.get(sections, options)  # 读取属性对应的值


