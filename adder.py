#!/usr/bin/python
# coding=utf-8

# Scalar function to read lines from files in a directory
# returns filename, line number, line

from pyUdx import Connection

connection=Connection()

a = connection.getParameter("a")
b = connection.getParameter("b")

result = a + b
print("a=%d b=%d result=%d" % (a,b,result))

return result
