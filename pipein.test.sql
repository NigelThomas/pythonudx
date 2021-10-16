set schema 'test';
set path 'test';

CREATE OR REPLACE VIEW  pipetest
as select stream * from stream(pipein(cursor(select stream * from dummy), '/usr/bin/gunzip -c /home/sqlstream/nigel/NOBACKUP/EDR-cricket/f_20210124_1.resorted.txt.gz'));

CREATE OR REPLACE VIEW pipetest2 AS
select stream floor(s.rowtime to second),count(*)
from pipetest s
group by floor(s.rowtime to second);


select stream s.rowtime,* from pipetest s;

