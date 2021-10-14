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

if rotation_period == 'MIDNIGHT':
    rotation_when = 'midnight'
elif rotation_period in ['W0','W1','W2','W3','W4','W5','W6']:
    rotation_when = rotation_period
else:
    # dealing with D/H/M/S
    rpsearch = re.search('([\d]+)([DdHhMmWw])',rotation_period)

    if rpsearch:
        rotation_when = rpsearch.group(2).upper()
        rotation_interval = int(rpsearch.group(1))

        # When to rotate first? Ideally we want to rotate on the next occurrence of a period
        # In SQL that would be STEP(current_time + <interval> BY <interval>)

        # timenow = datetime.now()

        # seconddelta = -timenow.second
        # microdelta = -timenow.microsecond

        # if rotation_when == 'D':
        #     # Rotate at next midnight
        #     daydelta = +1
        #     hourdelta = -timenow.hour
        #     minutedelta = -timenow.minute
        #     rotation_at = timenow + timedelta(days=daydelta,hours=hourdelta,minutes=minutedelta, seconds=seconddelta, microseconds=microdelta)

        # elif rotation_when == 'H':
        #     # Rotate at the next N hour boundary.
        #     hourdelta = rotation_interval - (timenow.hour % rotation_interval)
        #     minutedelta = -timenow.minute
        #     rotation_at = timenow + timedelta(hours=hourdelta,minutes=minutedelta, seconds=seconddelta, microseconds=microdelta)
        # elif rotation_when == 'M':
        #     # Rotate at the next N minute boundary
        #     minutedelta = rotation_interval - (timenow.minute % rotation_interval)
        #     rotation_at = timenow + timedelta(minutes=minutedelta, seconds=seconddelta, microseconds=microdelta)
        # elif rotation_when == 'S':
        #     # Rotate at the next N second boundary
        #     seconddelta = rotation_interval - (timenow.second % rotation_interval)
        #     rotation_at = timenow + timedelta(seconds=seconddelta, microseconds=microdelta)
    
        # rotation_at_time = rotation_at.time()
    else:
        # default - some unrecognized period - rotate at midnight
        rotation_when = 'midnight'



# if rotation_at_time:
#     log_handler = logging.handlers.TimedRotatingFileHandler(filename,when=rotation_when,interval=rotation_interval,atTime=rotation_at_time,backupCount=backup_count)
if rotation_interval:
    log_handler = logging.handlers.TimedRotatingFileHandler(filename,when=rotation_when,interval=rotation_interval,backupCount=backup_count)
else:
    log_handler = logging.handlers.TimedRotatingFileHandler(filename,when=rotation_when,backupCount=backup_count)

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
# if rotation_at:
#     logger.debug("rotation_at:"+str(rotation_at))
#     logger.debug("rotation_at_time:"+str(rotation_at_time))

rows = 0

while cursor.next():
    millis = int(round(time.time() * 1000))
    val = rowSliceGetter.value()
    rows += 1

    output = [str(v) for v in val]   
    message = ','.join(output)

    logger.info(message)
    out.executeUpdate(millis, message)
