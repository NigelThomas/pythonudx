create or replace schema test;
set schema 'test';
set path 'test';
 
create or replace stream dummy (dummy int);

drop function readfile;

create or replace function readfile(C cursor, "dirname" varchar(250), "fpattern" varchar(250))
returns table
( rowtime timestamp not null
, fname  varchar(100)
, line_no int
, line   varchar(100)
)
language EXTERNAL
no sql
no state
external name '/usr/bin/python3 /home/sqlstream/pyread/readfile.py';
 
 

