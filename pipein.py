#!/usr/bin/python
# coding=utf-8

# Table function to read the output from a command line pipe
# returns line by line, with a rowtime

from pyUdx import Connection
import time
from subprocess import Popen,PIPE

connection=Connection()
out = connection.getOutput()
cursor = connection.getInput(0)

commandString = connection.getParameter("command")
cmdarray = commandString.split()
print(str(cmdarray))

line_no = 0
with Popen(cmdarray, stdout=PIPE) as proc:
    for line in proc.stdout:
        line_no += 1
        if line_no % 1000 < 10:
            print(line_no)
            print(line)

        millis = int(round(time.time() * 1000))
        out.executeUpdate(millis, line.decode('utf-8').rstrip('\n'))
