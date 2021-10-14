#!/usr/bin/python
# coding=utf-8

# Stream function to read and passthrough any stream, and tee it to a log file
# It is acceptable to read from this view and simply pump to a native stream

# The log file is written by logger which allows us to benefit from rotating log handlers

import time
from datetime import datetime, timedelta
import logging
import logging.handlers
import re
from pyUdx import Connection
import sys

class WholeIntervalRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def computeRollover(self, currentTime):
        if self.when[0] == 'W' or self.when == 'MIDNIGHT':
            # use existing computation
            return super().computeRollover(currentTime)
        # round time up to nearest next multiple of the interval
        return ((currentTime // self.interval) + 1) * self.interval

connection=Connection()
out = connection.getOutput()
cursor = connection.getInput(0)

# This parameter allows us to choose which columns we write
rowSliceGetter = cursor.bind(connection.getParameter("WHICH"))

# These params are for the logging
filename = connection.getParameter("FILENAME")
backup_count = int(connection.getParameter("BACKUP_COUNT"))
rotation_period = connection.getParameter("ROTATION_PERIOD").upper()
# separate out the 'when' (which time period) and the 'interval' (how many of them)

rotation_interval = None
rotation_when = rotation_period

rpsearch = re.search('([\d]+)([DHMS])',rotation_period)

if rpsearch:
    rotation_when = rpsearch.group(2).upper()
    rotation_interval = int(rpsearch.group(1))

else:
    rotation_when = rotation_period
    if not rotation_period in ['W0','W1','W2','W3','W4','W5','W6']:
        # default - eithher midnight or some unrecognized period - rotate at midnight
        rotation_when = 'MIDNIGHT'

if rotation_interval:
    log_handler = WholeIntervalRotatingFileHandler(filename,when=rotation_when,interval=rotation_interval,backupCount=backup_count)
else:
    log_handler = WholeIntervalRotatingFileHandler(filename,when=rotation_when,backupCount=backup_count)

formatter = logging.Formatter('%(asctime)s,%(message)s')
formatter.converter = time.gmtime  # if you want UTC time
log_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

logger.debug("backupCount:"+str(backup_count))
logger.debug("rotation_when:"+rotation_when)
if rotation_interval:
    logger.debug("rotation_interval:"+str(rotation_interval))

logger.debug("next rollover at: "+str(datetime.utcfromtimestamp(log_handler.rolloverAt)))

rows = 0

while cursor.next():
    millis = int(round(time.time() * 1000))
    val = rowSliceGetter.value()
    rows += 1

    output = [str(v) for v in val]   
    message = ','.join(output)

    logger.info(message)
    out.executeUpdate(millis, message)
