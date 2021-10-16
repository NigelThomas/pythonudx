# pythonudx

This repository includes some example Python UDXs for SQLstream.


## pipein

This streaming UDX runs a command and reads its STDOUT, passing the lines back in a single "LINE" column until the command terminates.

This allows us to accomplish:
* Reading from a source type that isn't directly supported.
* Reading history at startup (read old files and then tail -F the latest file)
* Reading directly from a unix pipe

It would be quite easy to extend this to handle a command pipeline (each command pipes into the next command, and the final command pipes into the Python UDX).

And advantage of this approach is that pre-processing happens in a separate thread. So (for example) file decompression or decryption is happening in a separate thread from record parsing.

### Parameters
* Cursor - this is ignored - no rows are fetched
* Command - a command string which will be split (on spaces) and passed to subprocess.Popen

## readfile

This streaming UDX reads lines from files in a specified directory, and then exits

### Parameters
* Cursor - this is ignored - no rows are fetched
* Directory - absolute, or relative to the s-Server current working directory
* Filename Pattern - as required by `re.match` - so special characters may need escaping

##  writefile

This streaming UDX reads the input stream and emits ROWTIME and LINE where LINE is the concatenation of the columns mentioned in the WHICH parameter.

It relies on Python's `logging` module and uses `WholeIntervalRotatingFileHandler` which is a derivative of the `TimedRotatingFileHandler` borrowed from [Stack Overflow](https://stackoverflow.com/questions/53047922/python-handlers-timedrotatingfilehandler-rotation-does-not-work-as-i-expected). This lines up the file rotations, rounding to the nearest interval multiple.


### Parameters

* Cursor - the input data
* WHICH - a rowtype - for example row(col1, col2, col3) - these are the columns that will be concatenated
* filename = absolute or relative pathname for the logfile
* rotation_period = a number and unit, or a special case as shown below
* backup_count = how many file rotations to retain

You can specify rotation periods like so:
* 2H = 2 hours
* 3d = 3 days
* 30m = 30 minutes
* W0 = every Monday (W1 = Tuesday, ..., W6 = Sunday)
* midnight - rotate each midnight (UTC)

To run this in an application, pump the output into a native stream where it will be discarded; the file write happens as a side effect.

**NOTES:**
* 'midnight' rotates daily at midnight; 
* '1d' also rotates every day at midnight
* '12h' will rotate at noon and midnight; '6h' would also rotate at 6:00 and 18:00.
* '3d' rotates every third day at midnight. The first rotation will be the next day divisible by 3 according to the day of the month
* '5m' will rotate at hh:00, hh:05, etc
* '20s' will rotate at hh:mm:00, hh:mm:20, hh:mm:40 and so on



### Note on Output Formatting

The data is simply stringified (using Python's `str()` function) and concatenated (comma separated). If you are using complex types you may prefer (or need) to pre-format the output in SQL and then pass that single column to the UDX. See `writefile.test.sql` for an example.

Currently the message format includes the rowtime; to remove it, just remove asctime from the format:
```
formatter = logging.Formatter('%(asctime)s,%(message)s')
```
Becomes:
```
formatter = logging.Formatter('%(message)s')
```

If you need to include debugging messages into the log file, just change the configuration:
```
logger.setLevel(logging.INFO)
```
Becomes
```
logger.setLevel(logging.DEBUG)
```
