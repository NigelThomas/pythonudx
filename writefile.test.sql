set schema 'test';
set path 'test';

create or replace view serverstats as
select stream
        cast(measured_at as varchar(25))||','||
        case when is_running then 'T' else 'F' end ||','||
        cast(num_sessions as varchar(4))||','||
        cast(started_at as varchar(25))||','||
        cast(max_memory_bytes as varchar(15)) 
        as line 
from stream(getServerInfoForever(2));

create or replace view writeserverstats as
select stream * from stream(
    test.writefile
        (cursor (select stream line from serverstats)
        ,row(line),'/home/sqlstream/streamstats.log'
        ,'5m'
        ,20
        ));

select stream * from writeserverstats;
