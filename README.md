# pythonudx

This repository includes some example Python UDXs for SQLstream.


## readfile

This streaming UDX reads lines from files in a specified directory, and then exits

Parameters:
* Cursor - this is ignored - no rows are fetched
* Directory - absolute, or relative to the s-Server current working directory
* Filename Pattern - as required by `re.match` - so special characters may need escaping


