set schema 'test';
set path 'test';

select stream * from stream(pipein(cursor(select stream * from dummy), '/usr/bin/gunzip -c /home/sqlstream/nigel/NOBACKUP/EDR-cricket/f_20210124_1.resorted.txt.gz'));

