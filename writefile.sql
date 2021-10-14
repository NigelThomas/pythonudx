create or replace schema test;
set schema 'test';
set path 'test';
 

create or replace function writefile
    ( C cursor
    , WHICH select from C
    , filename VARCHAR(200)
    -- parameters for TimedRotatingFileHandler
    , rotation_period VARCHAR(4)    
    -- unit of time eg '30m','2H', '1D' or 'midnight' or 'W0','W1',...'W6' see https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler
    -- any unrecognized period is defaulted to 'midnight'
    , backup_count integer
    )
returns table
( ROWTIME TIMESTAMP
, line VARCHAR(1000)
)
language EXTERNAL
no sql
no state
external name '/usr/bin/python3 /home/sqlstream/pythonudx/writefile.py';
 
 

