create or replace schema test;
set schema 'test';
set path 'test';
 
create or replace stream dummy (dummy int);

drop function testtypes;

create or replace function testtypes(C cursor)
returns table
( rowtime timestamp not null
, db double
, bin binary(1000)
, vch varchar(1000)
)
language EXTERNAL
no sql
no state
external name '/usr/bin/python3 /home/sqlstream/pyread/readfile.py';
 
 