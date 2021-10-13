#!/usr/bin/python
# coding=utf-8

# Stream function to read and passthrough any stream, and add a column listing the data types

from pyUdx import Connection
import sys


connection=Connection()
out = connection.getOutput()
cursor = connection.getInput(0)
rowSliceGetter = cursor.bind(connection.getParameter("WHICH"))
rowlimit = connection.getParameter("ROWLIMIT")

rows = 0

while cursor.next():
    val = rowSliceGetter.value()
    rows += 1
    
    typelist = [str(type(v)).split("'")[1]+'::'+str(v) for v in val]
    out.executeUpdate(str(typelist))
    if rows >= rowlimit:
        break
