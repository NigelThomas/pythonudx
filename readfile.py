#!/usr/bin/python
# coding=utf-8

# Table function to read lines from files in a directory
# returns filename, line number, line

from pyUdx import Connection
import time
import os
import re

connection=Connection()
out = connection.getOutput()
cursor = connection.getInput(0)

fdir = connection.getParameter("dirname")
fpatString = connection.getParameter("fpattern")
fpat = re.compile(fpatString)

filenames = [f for f in os.listdir(fdir) if re.match(fpat, f)]
for fn in filenames:

    inFile = open(fdir+'/'+fn, "r")
    lines = inFile.read().split('\n')
    inFile.close()
    millis = int(round(time.time() * 1000))

    i = 0
    for line in lines:
        i += 1
        #printf("%s\n", line)
        out.executeUpdate(millis, fn, i, line)
