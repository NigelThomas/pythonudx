set schema 'test';
set path 'test';

!set force on
drop table types_tab;
!set force off


create table types_tab
( ti tinyint not null primary key
, si smallint
, i integer
, bi bigint
, vc varchar(10)
, ch char(10)
, b boolean
, ts timestamp
, tm time
, dt date
, ni numeric(3,0)
, nn numeric(5,3)
, deci decimal(5,0)
, decf  decimal(5,3)
, r real
, db double
, f float
);

insert into types_tab
( ti 
, si 
, i 
, bi 
, vc 
, ch 
, b 
, ts 
, tm 
, dt 
, ni 
, nn 
, deci 
, decf  
, r 
, db 
, f 
)
values
( 0
, 100
, 1200
, 3456789
, 'ABC'
, 'cdef'
, true
, timestamp '2021-01-01 12:34:56.789'
, time '12:34:56'
, date '2021-01-01'
, 3.0
, 5.23
, 52
, 47.6
, 123.456
, 234.567
, 345.678
);

select * from table(test.gettypes(cursor(select * from sys_boot.jdbc_metadata.columns_view),row(table_cat,data_type,sql_data_type),3));

select * from table(test.gettypes(cursor(select * from types_tab)
,row( ti 
, si 
, i 
, bi 
, vc 
, ch 
, b 
, ts 
, tm 
, dt 
, ni 
, nn 
, deci 
, decf  
, r 
, db 
, f 
),3
));
