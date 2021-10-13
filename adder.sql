create or replace schema test;
set schema 'test';
set path 'test';
 
!set force on
drop function adder;
!set force off

create or replace function adder("a" integer, "b" integer)
returns integer
language EXTERNAL
no sql
no state
external name '/usr/bin/python3 /home/sqlstream/pythonudx/adder.py';
 
 

