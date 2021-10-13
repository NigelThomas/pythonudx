#!/usr/bin/python
# coding=utf-8

# Table function to output data for test purposes

from pyUdx import Connection
import time
import os
import re

connection=Connection()
out = connection.getOutput()
cursor = connection.getInput(0)

# output data for (timestamp,) double, binary, varchar

outdata = [[ 1.23, "a test string".encode('utf-8'), "a test string" ]
, [2, "a test string", "a test string".encode('utf-8') ]
, ['3', 23, 45 ]
]

for i in range(outdata.length()):
    millis = int(round(time.time() * 1000))
    #printf("%s\n", line)
    out.executeUpdate(millis, outdata[i][0], outdata[i][1], outdata[i][2])
