#!/usr/bin/env python3
import os
import glob
import sys
from jsmin import jsmin


filepath = sys.argv[1]
jslists = (glob.glob(filepath+"*.js"))
for js in jslists:
    with open(js,"r+",encoding="utf-8") as jsfile:
        minified = jsmin(jsfile.read())
    jsfile.close()

    with open(js,"w",encoding="utf-8") as jsfile:
        jsfile.write(minified)
    jsfile.close()
