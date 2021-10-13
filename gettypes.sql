create or replace schema test;
set schema 'test';
set path 'test';
 
!set force on
drop function gettypes;
!set force off

create or replace function gettypes(C cursor, WHICH select from C, rowlimit integer)
returns table
( C.* passthrough
, "types" VARCHAR(1000)
)
language EXTERNAL
no sql
no state
external name '/usr/bin/python3 /home/sqlstream/pyread/gettypes.py';
 
 

