create or replace schema test;
set schema 'test';
set path 'test';
 
create or replace stream dummy (dummy int);


create or replace function pipein(C cursor, "command" varchar(500))
returns table
( rowtime timestamp not null
, input_line   varchar(1000)
)
language EXTERNAL
no sql
no state
external name '/usr/bin/python3 /home/sqlstream/pythonudx/pipein.py';
 
 

