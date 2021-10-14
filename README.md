# pythonudx

This repository includes some example Python UDXs for SQLstream.


## readfile

This streaming UDX reads lines from files in a specified directory, and then exits

### Parameters
* Cursor - this is ignored - no rows are fetched
* Directory - absolute, or relative to the s-Server current working directory
* Filename Pattern - as required by `re.match` - so special characters may need escaping

##  writefile

This streaming UDX reads the input stream and emits ROWTIME and LINE where LINE is the concatenation of the columns mentioned in the WHICH parameter.

It relies on Python's `logging` and uses the `TimedRotatingFileHandler`.


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
* W0 = every Sunday (W1 = Monday, W6 = Saturday)
* midnight - rotate each midnight (UTC)

To run this in an application, pump the output into a native stream where it will be discarded; the file write happens as a side effect.

**NOTES:**
* 'midnight' rotates at midnight; '1d' rotates 24 hours after the start, and every 24 hours after that.
* '5m' will rotate 5 minutes after start time, not at :00, :05, etc
* See 


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
