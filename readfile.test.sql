set schema 'test';
set path 'test';

select stream * from stream(readfile(cursor(select stream * from dummy), '/home/sqlstream/pythonudx','.*.sql'));
